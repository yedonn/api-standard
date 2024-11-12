import datetime
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import generate_otp, is_contact, is_email
from app.core.auth import create_token, get_hashed_password, verify_password, verify_token, verify_refresh_token
from app.schemas.auth import Auth, LoginForm, AuthToken, OtpForm, ResetPasswordForm, TokenRead, VerifyForm
from app.schemas.session import SessionCreate, SessionUpdate
from app.schemas.otp import OtpCreate, OtpUpdate
from app.api.v1.endpoints.device_endpoint import save_device_info
from app.api.v1.endpoints.user_endpoint import UserUpdate
from app.api.v1.dependencies import get_session_service, get_user_service, get_device_service, get_otp_service, OtpService, DeviceService, SessionService, UserService
from app.utilities.global_utils import create_error_response, create_success_response

router = APIRouter()

@router.post("/login", name="Connexion des utilisateurs", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def login(
    request: Request, 
    payload: LoginForm,
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service),
    device_service: DeviceService = Depends(get_device_service)
):
    client_ip = request.client.host
    
    # Vérification des identifiants (email, contact, ou numéro de compte)
    if is_email(payload.username):
        user = await user_service.get_user_by_field('email', payload.username)
    elif is_contact(payload.username):
        user = await user_service.get_user_by_field('contact', payload.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Identifiant invalide."
        )

    # Gestion des erreurs de login
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Login incorrect."
        )
    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Mot de passe incorrect."
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Votre compte est désactivé. Veuillez contacter un administrateur."
        )
    
    # Enregistrer ou mettre à jour les informations du périphérique
    device = await save_device_info(user.id, request, device_service)

    sessions = await session_service.filter_internal_sessions({"user_id": user.id, "device_id": device.id, "host":client_ip})

    for session in sessions:
        if session.expires_at > datetime.datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Vous avez une session est toujours active."
            )
        else:
            await session_service.update_internal_session(session.id, SessionUpdate(is_active=False))
        
    
    
    # Création des tokens JWT (access token + refresh token)
    token_data = AuthToken(id=user.id)
    token = create_token(token_data)

    # Création de la nouvelle session
    session_data = SessionCreate(
        user_id=user.id,
        device_id=device.id,
        is_active=True,
        host=client_ip,
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        expires_at=token['expire']
    )
    
    await session_service.create_session(session_data)

    # Retour des tokens à l'utilisateur
    return token

@router.post("/request-otp", name="Demande de code OTP", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def request_otp(
    request: Request, 
    payload: VerifyForm,
    user_service: UserService = Depends(get_user_service),
    otp_service: OtpService = Depends(get_otp_service)
):
    # Vérification des identifiants (email, contact, ou numéro de compte)
    if is_email(payload.username):
        user = await user_service.get_user_by_field('email', payload.username)
    elif is_contact(payload.username):
        user = await user_service.get_user_by_field('contact', payload.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Identifiant invalide."
        )
    
    otps = await otp_service.filter_internal_otps({"user_id": user.id, "verified": False})

    for otp in otps:
        if otp.expires_at < datetime.datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le code OTP transmis est toujours valide."
            )

    # Générer et stocker l'OTP
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # OTP valide pendant 10 minutes
    otp = OtpCreate(user_id=user.id, otp_code=generate_otp(), expires_at=expiration_time)

    await otp_service.create_otp(otp)

    # Appel au service d'envoi de l'OTP par email/SMS
    # await send_otp_via_email_or_sms(data.email, otp)  # Implémentez cette fonction

    return create_success_response(
        message=f"Un code OTP vous sera transmis sous peu par mail à l'adresse : {user.email}."
    )

@router.post("/verify-otp", name="Vérification du code OTP", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def verify_otp(
    request: Request, 
    payload: OtpForm,
    user_service: UserService = Depends(get_user_service),
    otp_service: OtpService = Depends(get_otp_service)
):
    # Vérification des identifiants (email, contact, ou numéro de compte)
    if is_email(payload.username):
        user = await user_service.get_user_by_field('email', payload.username)
    elif is_contact(payload.username):
        user = await user_service.get_user_by_field('contact', payload.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Identifiant invalide."
        )
    
    otps = await otp_service.filter_internal_otps({"user_id": user.id, "otp_code": payload.otp_code, "verified": False})

    if not otps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le Code OTP est invalide."
        )

    for otp in otps:
        if not otp.expires_at < datetime.datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le code OTP a expiré."
            )
        otp_data =  otp
        break;
        
    otp = OtpUpdate(verified=True)

    await otp_service.update_otp(otp_data.id, otp)

    return create_success_response(
        message=f"Le code OTP est valide."
    )

@router.put("/reset-password", name="Vérification du code OTP", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def reset_password(
    request: Request, 
    payload: ResetPasswordForm,
    user_service: UserService = Depends(get_user_service)
):
    # Vérification des identifiants (email, contact, ou numéro de compte)
    if is_email(payload.username):
        user = await user_service.get_user_by_field('email', payload.username)
    elif is_contact(payload.username):
        user = await user_service.get_user_by_field('contact', payload.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Identifiant invalide."
        )
    
    if not payload.password == payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Les mots de passe ne sont pas conforment."
        )
    
    reset_password_data = UserUpdate(password=get_hashed_password(payload.password))
    user_update = await user_service.update_user(user.id,reset_password_data)

    return create_success_response(
        message=f"Le mot de passe a été réinitialisé.",
        data=user_update
    )


@router.post("/refresh-token", name="Rafraîchir le token", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def refresh_token(
    token: Annotated[str, Depends(verify_refresh_token)],  # Vérification du token
    session_service: SessionService = Depends(get_session_service)
):
    # Récupération des sessions actives
    session = await session_service.get_internal_session_by_field("refresh_token", token)

    # Vérification si des sessions existent
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session non trouvée."
        )
    
    if not session.is_active :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session inactive."
        )
    
    # Créer un nouveau access_token et refresh_token
    token = create_token(AuthToken(id=session.user_id))
    
    # Mise à jour de la session avec les nouveaux tokens
    await session_service.update_session(
        session.id, 
        SessionUpdate(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_at=token["expire"]  # Mettez à jour avec la bonne valeur
        )
    )
    
    # Retourner le nouveau token
    return token

@router.post("/revoke-token", name="Deconnexion d'une session", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def revoke_token(token: Annotated[str, Depends(verify_token)], session_service: SessionService = Depends(get_session_service)):
        
    session = await session_service.get_internal_session_by_field("access_token", token)

    if not session :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session introvable."
        )
    
    if not session.is_active :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session inactive."
        )
    
    await session_service.update_session(session.id, SessionUpdate(is_active=False))
    return {
            "message": "Session deconnectée avec succès.",
            "status": status.HTTP_200_OK,
        }

@router.get("/verify-token", name="Vérifier la validité du token", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def verify_access_token(token: Annotated[str, Depends(verify_token)], session_service: SessionService = Depends(get_session_service)):
        
    session = await session_service.get_internal_session_by_field("access_token", token)

    if not session :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session introvable."
        )
    
    if not session.is_active :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session inactive."
        )

    return create_success_response(
        message="Token valide.",
        data=session
    )