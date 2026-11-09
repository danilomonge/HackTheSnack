package de.pecus.api.vo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Clase de transporte de errores de servicios
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 */
@JsonIgnoreProperties({"exception"})
public class ResponseErrorVO {

    /**
     * Codigo de error
     */
    private String code;

    /**
     * Clave del error
     */
    private String key;

    /**
     * Mensaje de error
     */
    private String message;
    
    /**
     * Excepcion de la respuesta
     */
    private Throwable exception;

    /**
     * Constructor default
     */
    public ResponseErrorVO() {

    }

    /**
     * Constructor con parametros
     * 
     * @param code    Codigo de error
     * @param message Mensaje de error
     */
    public ResponseErrorVO(String code, String keyName, String message, Throwable exception) {
        super();
        this.code = code;
        this.key = keyName;
        this.message = message;
        this.exception = exception;
    }

    /**
     * @return the code
     */
    public String getCode() {
        return code;
    }

    /**
     * @param code the code to set
     */
    public void setCode(String code) {
        this.code = code;
    }
    
    /**
     * @return the key name
     */
    public String getKey() {
        return key;
    }

    /**
     * @param the key name
     */
    public void setKey(String key) {
        this.key = key;
    }

    /**
     * @return the message
     */
    public String getMessage() {
        return message;
    }

    /**
     * @param message the message to set
     */
    public void setMessage(String message) {
        this.message = message;
    }

    /**
     * @return the exception
     */
    public Throwable getException() {
        return exception;
    }

    /**
     * @param exception catched
     */
    public void setException(Throwable exception) {
        this.exception = exception;
    }

    @Override
    public String toString() {
        return "ResponseErrorVO [code=" + code + ", message=" + message + "]";
    }

}
