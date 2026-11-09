package de.pecus.api.exception;

import java.text.MessageFormat;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import de.pecus.api.constant.GeneralConstants;
import de.pecus.api.error.BusinessError;
import de.pecus.api.vo.ResponseErrorVO;

/**
 * Excepcion para manejo de errores de las aplicaciones 
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 */
public class GeneralException extends RuntimeException {

    /**
     * Serial Version UID
     */
    private static final long serialVersionUID = 8078621487299359131L;
    
    /**
     * Codigo de error
     */
    private final String code;
    
    /**
     * Parametros causa de excepcion
     */
    private final Object[] params;
    
    /**
     * Constructor default
     */
    public GeneralException() {
        super();
        this.code = GeneralConstants.DEFAULT_ERROR_CODE;
        params = new Object[0];
    }
    
    /**
     * Constructor con error de negocio y causa
     * @param message Mensaje de excepcion
     * @param cause Causa de la excepcion
     */
    public GeneralException(String message, Throwable cause, Object... params) {
        super(message, cause);
        this.params = params;
        this.code = GeneralConstants.DEFAULT_ERROR_CODE;
    }
    
    /**
     * Constructor con error de negocio y causa
     * @param message Mensaje de excepcion
     * @param cause Causa de la excepcion
     * @param code Codigo de error
     */
    public GeneralException(BusinessError businessError, Throwable cause, Object... params) {
        super(MessageFormat.format(businessError.getDescription(), params), cause);
        this.params = params;
        this.code = businessError.getCode();
    }
    
    /**
     * Constructor con error de negocio y causa
     * @param businessError Mensaje de excepcion
     * @param params Parametros para configurar la excepcion
     */
    public GeneralException(BusinessError businessError, Object... params) {
        super(MessageFormat.format(businessError.getDescription(), params));
        this.params = params;
        this.code = businessError.getCode();
    }
    
    /**
     * Constructor con lista de errores de negocio con formato
     * @param responseErrorLit lista de mensajes de negocio con formato 
     */
    public GeneralException(List<ResponseErrorVO> responseErrorList) {
        
        super(Arrays.asList(responseErrorList).stream()
                .map(n -> String.valueOf(n))
                .collect(Collectors.joining(",", "{", "}")));
        this.params = null;
        this.code = null;
    }
    
    /**
     * @return the params
     */
    public Object[] getParams() {
        return params;
    }

    /**
     * @return the code
     */
    public String getCode() {
        return code;
    }

}
