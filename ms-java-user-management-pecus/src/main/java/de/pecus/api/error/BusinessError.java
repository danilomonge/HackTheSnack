package de.pecus.api.error;

/**
 * Clase para identificar errores de negocio
 * 
 */
public class BusinessError {

    private String code;
    
    private String key;

    private String description;

    private Object[] descriptionArgs;

    /**
     * Constructor default
     */
    public BusinessError() {
        super();
    }

    /**
     * Constructor con parametros
     * 
     * @param code
     * @param description
     * @param descriptionArgs
     */
    public BusinessError(String code, String key, String description, Object... descriptionArgs) {
        super();
        this.code = code;
        this.description = description;
        this.key = key;
        this.descriptionArgs = descriptionArgs;
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
     * @return the description
     */
    public String getDescription() {
        return description;
    }

    /**
     * @param description the description to set
     */
    public void setDescription(String description) {
        this.description = description;
    }
    
    /**
     * @return the key
     */
    public String getKey() {
        return key;
    }
    
    /**
     * @param the key
     */
    public void setKey(String key) {
        this.key = key;
    }

    /**
     * @return the descriptionArgs
     */
    public Object[] getDescriptionArgs() {
        return descriptionArgs;
    }

    /**
     * @param descriptionArgs the descriptionArgs to set
     */
    public void setDescriptionArgs(Object[] descriptionArgs) {
        this.descriptionArgs = descriptionArgs;
    }

}
