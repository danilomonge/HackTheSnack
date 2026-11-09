package de.pecus.api.error;

/**
 * Enumeracion para manejo de errores.
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public final class GeneralBusinessErrors {

    private GeneralBusinessErrors() {
        // No debe instanciarse
    }

    /* File errors */
    public static final String FILE_NOT_FOUND = "FILE_NOT_FOUND";

    public static final String MIN_VALUE_PAGE_NUMBER_ERROR = "MIN_VALUE_PAGE_NUMBER_ERROR";

    public static final String MIN_VALUE_PAGE_SIZE_ERROR = "MIN_VALUE_PAGE_SIZE_ERROR";

    public static final String REQUIRED_PAGE_NUMBER_ERROR = "REQUIRED_PAGE_NUMBER_ERROR";

    public static final String REQUIRED_PAGE_SIZE_ERROR = "REQUIRED_PAGE_SIZE_ERROR";

    public static final String REQUIRED_PARAMETERS_ERROR = "REQUIRED_PARAMETERS_ERROR";
    
    public static final String REQUIRED_IS_AUTOMATICO = "REQUIRED_IS_AUTOMATICO";

    public static final String NOT_FOUND_ENVIRONMENT_VAR = "NOT_FOUND_ENVIRONMENT_VAR";

    public static final String ELAPSED_TIME = "ELAPSED_TIME";

    public static final String LOG4J_REQUIRED_URL_ERROR = "LOG4J_REQUIRED_URL_ERROR";

    public static final String LOG4J_REQUIRED_USER_ERROR = "LOG4J_REQUIRED_USER_ERROR";

    public static final String LOG4J_REQUIRED_PASSWORD_ERROR = "LOG4J_REQUIRED_PASSWORD_ERROR";

    public static final String LOG4J_REQUIRED_VALIDATION_QUERY_ERROR = "LOG4J_REQUIRED_VALIDATION_QUERY_ERROR";
    
    public static final String FUNCTION_NOT_AUTHORIZED = "FUNCTION_NOT_AUTHORIZED";
    
	public static final String INVALID_TOKEN_ERROR = "INVALID_TOKEN_ERROR";
    
    public static final String REQUIRED_COMPONENTE_ERROR = "REQUIRED_COMPONENTE_ERROR";
    
    public static final String REQUIRED_TIPO_COMPONENTE_ERROR = "REQUIRED_TIPO_COMPONENTE_ERROR";
    
    public static final String BUSINESS_ERROR_NOT_FOUND = "BUSINESS_ERROR_NOT_FOUND";
    
    public static final String GENERIC_ERROR_KEY_SERVICE = "GENERIC_ERROR_KEY_SERVICE";
    
    public static final String DATA_NOT_FOUND = "DATA_NOT_FOUND";
    
}
