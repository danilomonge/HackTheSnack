package de.pecus.api.util;

import static de.pecus.api.error.BusinessErrorUtil.getBusinessError;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import de.pecus.api.constant.GeneralConstants;
import de.pecus.api.error.BusinessError;
import de.pecus.api.error.BusinessErrorUtil;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.exception.PecusException;
//import de.pecus.api.log.SmartLogger;
//import de.pecus.api.log.SmartLoggerFactory;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseErrorVO;
import de.pecus.api.vo.ResponseVO;

/**
 * Clase para manejo de respuestas de servicios
 *
 * @author Luis Enrique Sanchez Santiago
 *
 */
public class ResponseUtil {

    /**
     * SmartLogger
     */
    //private static final SmartLogger SMART_LOGGER = SmartLoggerFactory.getLogger(ResponseUtil.class);
    /**
     * Slf4jLogger
     */
    private static final Logger LOGGER = LoggerFactory.getLogger(ResponseUtil.class);

	private ResponseUtil (){
        throw new IllegalStateException("Utility class");
    }

    /**
     * Obtiene una respuesta a partir de una excepcion, para unificar las
     * respuestas con un mensaje
     *
     * @param <T> Clase especifica de la respuesta
     * @param exception Excepcion a manejar
     * @return Respuesta con errores u objeto de acuerdo al tipo de excepcion
     */
    public static <T> ResponseVO<T> getErrorResponse( Exception exception) {

        ResponseVO<T> response = new ResponseVO<>();
        List<ResponseErrorVO> errors = new ArrayList<>();

        response.setSuccess(false);

        // Si la excepcion lanzada es de tipo PecusException
        if( exception instanceof PecusException ) {
            PecusException PecusException = (PecusException)exception;
            if(ValidatorUtil.isNullOrEmpty(PecusException.getResponseErrorList())) {
                // Se genero una excepcion de la aplicacion, pero no se controlo
                errors.add( new ResponseErrorVO(GeneralConstants.GENERAL_ERROR_CODE, GeneralConstants.GENERAL_ERROR_KEY, PecusException.getMessage(), PecusException) );
            } else {
                // La excepcion se controlo correctamente
                errors.addAll(PecusException.getResponseErrorList());
            }
        } else {
        	LOGGER.error("Error no controlado:::: ", exception);
            // Se genero una excepcion de cualquier otro tipo y no se controlo
            errors.add( new ResponseErrorVO(GeneralConstants.GENERAL_ERROR_CODE, GeneralConstants.GENERAL_ERROR_KEY, GeneralConstants.GENERAL_ERROR_MESSAGE, exception) );
        }
        response.setErrors(errors);
        return response;
    }

    /**
     * Agrega un elemento a la lista de errores de la respuesta cuando ocurre un error de negocio
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
    @SuppressWarnings("rawtypes")
	public static <T> void addError(RequestVO request, ResponseVO<T> response,
            String businessErrorName, Throwable throwable, Object... params) {
        BusinessError businessError = getBusinessError(businessErrorName, request.getIdioma());
        if(ValidatorUtil.isNull(response)) {
            response = new ResponseVO<>();
        }
        if(ValidatorUtil.isNull(response.getErrors())) {
            response.setErrors( new ArrayList<ResponseErrorVO>() );
        }
        if(ValidatorUtil.isNull(businessError)) {
            businessError = BusinessErrorUtil.getBusinessError(GeneralBusinessErrors.BUSINESS_ERROR_NOT_FOUND, request.getIdioma());
            response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                    businessError.getKey(),
                    MessageFormat.format(businessError.getDescription(), businessErrorName), throwable));
            //SMART_LOGGER.businessError(request, businessError, throwable, businessErrorName);
        } else {
            response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                    businessError.getKey(),
                    MessageFormat.format(businessError.getDescription(), params), throwable));
            //SMART_LOGGER.businessError(request, businessError, throwable, params);
        }
        
    }

    /**
     * Agrega un elemento a la lista de errores de la respuesta
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
    @SuppressWarnings("rawtypes")
	public static <T> void addError(RequestVO request, ResponseVO<T> response,
            String businessErrorName, Object... params) {
        addError(request, response, businessErrorName, null, params);
    }

    /**
     * Agrega un elemento a la lista de errores de la respuesta cuando ocurre una excepción
     * sólo en el login
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
    @SuppressWarnings("rawtypes")
	public static <T> void addErrorWithoutToken(RequestVO request, ResponseVO<T> response,
            String  businessErrorName, Object... params) {
    	BusinessError businessError = getBusinessError(businessErrorName, request.getIdioma());
        if(response.getErrors() == null) {
            response.setErrors( new ArrayList<ResponseErrorVO>() );
        }
        response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                businessError.getKey(),
                businessError.getDescription(), null));
        //SMART_LOGGER.businessError(request, businessError, null, params);
    }

	@SuppressWarnings("rawtypes")
	public static <T> void addErrors(RequestVO request, ResponseVO<T> response, List<ResponseErrorVO> errors) {
		if(!ValidatorUtil.isNullOrEmpty(errors)) {
			for(ResponseErrorVO error : errors) {
				ResponseUtil.addError(request, response, error.getKey());
			}
		}
	}
	
	public static void removeAllErrors(ResponseVO<?> response) {
		response.setErrors(new ArrayList<ResponseErrorVO>());
	}
	
	/* ***************************************************
	 * Inician metodos sin RequestVO
	 * ***************************************************/

    /**
     * Agrega un elemento a la lista de errores de la respuesta cuando ocurre un error de negocio
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
	public static <T> void addError(ResponseVO<T> response,
            String businessErrorName, String idioma, Throwable throwable, Object... params) {
        BusinessError businessError = getBusinessError(businessErrorName, idioma);
        if(ValidatorUtil.isNull(response)) {
            response = new ResponseVO<>();
        }
        if(ValidatorUtil.isNull(response.getErrors())) {
            response.setErrors( new ArrayList<ResponseErrorVO>() );
        }
        if(ValidatorUtil.isNull(businessError)) {
            businessError = BusinessErrorUtil.getBusinessError(GeneralBusinessErrors.BUSINESS_ERROR_NOT_FOUND, idioma);
            String error = MessageFormat.format(businessError.getDescription(), businessErrorName);
            response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                    businessError.getKey(), error, throwable));
            LOGGER.error(error, throwable);
        } else {
        	String error = MessageFormat.format(businessError.getDescription(), params);
            response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                    businessError.getKey(), error, throwable));
            LOGGER.error(error, throwable);
        }
    }

    /**
     * Agrega un elemento a la lista de errores de la respuesta
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
	public static <T> void addError(ResponseVO<T> response,
            String businessErrorName, String idioma, Object... params) {
        addError(response, businessErrorName, idioma, null, params);
    }

    /**
     * Agrega un elemento a la lista de errores de la respuesta cuando ocurre una excepción
     * sólo en el login
     * @param <T> Clase especifica de la respuesta
     * @param response Objeto de respuesta
     */
	public static <T> void addErrorWithoutToken(ResponseVO<T> response,
            String  businessErrorName, String idioma, Object... params) {
    	BusinessError businessError = getBusinessError(businessErrorName, idioma);
        if(response.getErrors() == null) {
            response.setErrors( new ArrayList<ResponseErrorVO>() );
        }
        String error = MessageFormat.format(businessError.getDescription(), params);
        response.getErrors().add(new ResponseErrorVO(businessError.getCode(),
                businessError.getKey(),
                businessError.getDescription(), null));
        LOGGER.error(error);
    }

	public static <T> void addErrors(ResponseVO<T> response, String idioma, List<ResponseErrorVO> errors) {
		if(!ValidatorUtil.isNullOrEmpty(errors)) {
			for(ResponseErrorVO error : errors) {
				ResponseUtil.addError(response, error.getKey(), idioma);
			}
		}
	}

}
