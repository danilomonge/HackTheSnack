package de.pecus.api.util;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.error.UsuarioBusinessErrors;
import de.pecus.api.vo.ResponseErrorVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.usuarios.FindDetailUsuarioResponseVO;
import de.pecus.api.vo.usuarios.FindListUsuarioResponseVO;

public class UsuarioMobileResponseBuilder {

	public static final ResponseEntity<ResponseVO<Long>> buildCreateUserResponse(ResponseVO<Long> serviceResponse) {
		ResponseEntity<ResponseVO<Long>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.CREATED).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.INVALID_EMAIL_FORMAT_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.DUPLICATED_USER_ID_EMAIL_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_USER_ID_MOBILE_NUMBER_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.DUPLICATED_USER_MOBILE_NUMBER_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.EXIST_PATIENT_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.EXIST_PERSON_ERROR)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}

	public static final ResponseEntity<ResponseVO<String>> buildUpdatePasswordResponse(
			ResponseVO<String> serviceResponse) {
		ResponseEntity<ResponseVO<String>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_EMAIL_OR_PHONE)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_PASSWORD_NUEVO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}

	
	public static final ResponseEntity<ResponseVO<String>> buildResetPasswordResponse(
			ResponseVO<String> serviceResponse) {
		ResponseEntity<ResponseVO<String>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_USER_ID_EMAIL_ERROR)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}
	
	public static final ResponseEntity<ResponseVO<Long>> buildAddRolUserResponse(ResponseVO<Long> serviceResponse) {
		ResponseEntity<ResponseVO<Long>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_ID_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_ROL_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_DOCTOR_ID)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_ROL_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}

	public static final ResponseEntity<ResponseVO<Boolean>> buildAsignarTokenResponse(
			ResponseVO<Boolean> serviceResponse) {
		ResponseEntity<ResponseVO<Boolean>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_USER_ID_MOBILE_NUMBER_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_TOKEN_ERROR)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}
	
	
	public static final ResponseEntity<ResponseVO<FindDetailUsuarioResponseVO>> buildFindDetailUsuarioResponse(
			ResponseVO<FindDetailUsuarioResponseVO> serviceResponse) {
		ResponseEntity<ResponseVO<FindDetailUsuarioResponseVO>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR) || responseErrorVO
						.getKey().equals(UsuarioBusinessErrors.REQUIRED_ID_USUARIO)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}
	
	public static final ResponseEntity<ResponseVO<Boolean>> buildDeleteUsuarioResponse(
			ResponseVO<Boolean> serviceResponse) {
		ResponseEntity<ResponseVO<Boolean>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)
						|| responseErrorVO.getKey().equals(UsuarioBusinessErrors.REQUIRED_ID_USUARIO)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}
	
	public static final ResponseEntity<ResponseVO<List<FindListUsuarioResponseVO>>> buildFindListUsuarioResponse(
			ResponseVO<List<FindListUsuarioResponseVO>> serviceResponse) {
		ResponseEntity<ResponseVO<List<FindListUsuarioResponseVO>>> response = null;
		if (ValidatorUtil.isSuccessfulResponse(serviceResponse)) {
			response = ResponseEntity.status(HttpStatus.OK).body(serviceResponse);
		} else {
			for (ResponseErrorVO responseErrorVO : serviceResponse.getErrors()) {
				if (responseErrorVO.getKey().equals(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR)) {
					response = ResponseEntity.status(HttpStatus.BAD_REQUEST).body(serviceResponse);
					break;
				} else if (responseErrorVO.getKey().equals(UsuarioBusinessErrors.NOT_FOUND_USUARIO_ERROR)) {
					response = ResponseEntity.status(HttpStatus.NOT_FOUND).body(serviceResponse);
					break;
				} else {
					response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(serviceResponse);
					break;
				}
			}
		}
		return response;
	}
	
	
}
