package de.pecus.api.util;

import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.exception.PecusException;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;

/**
 * Clase de utileria para validacion
 * 
 */
public final class ValidatorArqUtil {

    /**
     * Valida los parametros de paginacion
     * 
     * @param <T> Objeto de parametros de request
     * @param <K> Objeto de de datos de respuesta
     * @param request Objeto de request
     * @param response Objeto de response
     */
    public static <T, K> void validatePaginatonParameters(RequestVO<T> request, ResponseVO<K> response) {
        if(ValidatorUtil.isNull(request.getPage())) {
            ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PAGE_NUMBER_ERROR, request);
        } 
        else if(!ValidatorUtil.isGreaterThanZero(request.getPage())) {
        	ResponseUtil.addError(request, response, GeneralBusinessErrors.MIN_VALUE_PAGE_NUMBER_ERROR, request);
        }
        if(ValidatorUtil.isNull(request.getSize())) {
            ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PAGE_SIZE_ERROR, request);
        }
        else if(!ValidatorUtil.isGreaterThanZero(request.getSize())) {
            ResponseUtil.addError(request, response, GeneralBusinessErrors.MIN_VALUE_PAGE_SIZE_ERROR, request);
        }
        if (!ValidatorUtil.isSuccessfulResponse(response)) {
        	throw new PecusException(response.getErrors());
        }
    }
    
    public static <T, K> boolean validateParameters(RequestVO<T> request, ResponseVO<K> response) {
        if (ValidatorUtil.isNull(request.getParameters())) {
        	throw new PecusException(GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR, request.getIdioma());
        }
        return true;
    }
    
}
