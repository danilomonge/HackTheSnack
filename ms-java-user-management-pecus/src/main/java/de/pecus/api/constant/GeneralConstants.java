package de.pecus.api.constant;

import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import org.apache.commons.lang3.time.FastDateFormat;

/**
 * Clase de constantes
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public final class GeneralConstants {
    
    /**
     * Default parameters for pagination
     */
    public static final int INITIAL_PAGE = 1;
    public static final int INITIAL_SIZE = 10;

    /**
     * Archivo con las propiedades de conexión a la base de datos en la variable de
     * entorno
     */
    public static final String SMART_LOGGER_DB_CREDENTIALS_ENV_VARIABLE = "SMARTLOGGER_DB_CREDENTIALS";

    /**
     * Archivo con las propiedades de conexión a la base de datos
     */
    public static final String SMART_LOGGER_DB_CREDENTIALS_CLASSPATH = "db-credentials.json";

    /**
     * Prefix used to identify smartlogger database connection properties
     */
    public static final String SMART_LOGGER_DB_PROPERTY_PREFIX = "smartlogger.db.";

    /**
     * Property key name part of audit database
     */
    public static final String SMART_LOGGER_AUDIT_PROPERTY = "audit.";

    /**
     * Property key name part of business_error database
     */
    public static final String SMART_LOGGER_BUSINESS_ERROR_PROPERTY = "business_error.";
    
    /**
     * Property key name part of client_error database
     */
    public static final String SMART_LOGGER_CLIENT_ERROR_PROPERTY = "client_error.";

    /**
     * Property key name part of error database
     */
    public static final String SMART_LOGGER_ERROR_PROPERTY = "error.";

    /**
     * Property key name part of debug database
     */
    public static final String SMART_LOGGER_DEBUG_PROPERTY = "debug.";

    /**
     * Property key name part of measure database
     */
    public static final String SMART_LOGGER_MEASURE_PROPERTY = "measure.";
    
    /**
     * Property key name part of PECUS database
     */
    public static final String SMART_LOGGER_PECUS_PROPERTY = "pecus.";

    /**
     * Property suffix for logger database URL
     */
    public static final String SMART_LOGGER_DB_URL_SUFIX = "url";

    /**
     * Property suffix for logger database user name
     */
    public static final String SMART_LOGGER_DB_USER_SUFIX = "user";

    /**
     * Property suffix for logger database password
     */
    public static final String SMART_LOGGER_DB_PASSWORD_SUFIX = "pass";

    /**
     * Property suffix for logger database driver
     */
    public static final String SMART_LOGGER_DB_DRIVER_SUFIX = "driver";

    /**
     * Property suffix for logger database validation query
     */
    public static final String SMART_LOGGER_DB_VALIDATION_QUERY_SUFIX = "validationQuery";

    /**
     * Tamanno minimo para el atributo Descripcion
     */
    public static final int MIN_SIZE_DESCRIPCION = 2;

    /**
     * Tamanno maximo para el atributo Descripcion
     */
    public static final int MAX_SIZE_DESCRIPCION = 100;

    /**
     * Usuario default
     */
    public static final Long SYSTEM_USER = 0L;

    /**
     * Constante cero
     */
    public static final int ZERO = 0;

    /**
     * Constante cero
     */
    public static final long ZERO_LONG = 0;
    
    /**
     * Constante de cero tipo String
     */
    public static final String ZERO_STRING = "0";
    
    
    /**
     * Constante cero
     */
    public static final char ZERO_CHAR= '0';

    /**
     * Constante null string
     */
    public static final String NULL = "null";

    /**
     * Constante uno
     */
    public static final int ONE = 1;

    /**
     * Constante uno
     */
    public static final long ONE_LONG = 1L;
    
    /**
     * Constante cien
     */
    public static final int ONE_HUNDRED = 100;

    /**
     * Cadena vacia
     */
    public static final String EMPTY_STRING = "";

    /**
     * Archivo de properties generales
     */
    public static final String GENERAL_PROPERTIES_FILE = "GeneralBusinessError.properties";

    /**
     * Archivo de properties del proyecto específico
     */
    public static final String PROPERTIES_FILE = "BusinessError.properties";
    
    /**
     * Archivo de properties del proyecto específico en ingles
     */
    public static final String PROPERTIES_FILE_EN = "BusinessErrorEn.properties";
    
    public static final String IDIOMA_ES_MX = "es_MX";
    
    public static final String IDIOMA_EN_US = "en_US";
    
    public static final Map<String, String> IDIOMAS_LIST;
    static {
    	IDIOMAS_LIST = new HashMap<>();
    	IDIOMAS_LIST.put("es_MX", "GeneralBusinessError.properties, ArchitectureBusinessError.properties, BusinessError.properties");
    	IDIOMAS_LIST.put("en_US", "GeneralBusinessErrorEn.properties, ArchitectureBusinessErrorEn.properties, BusinessErrorEn.properties");
    }
    
    public static final String PROPERTY_FILE_SEPARATOR = ",";

    /**
     * Separador de properties de errores de negocio
     */
    public static final String PROPERTY_SEPARATOR = ":";

    /**
     * Codigo de error generico
     */
    public static final String GENERAL_ERROR_CODE = "-1";

    /**
     * Codigo de error generico
     */
    public static final String GENERAL_ERROR_KEY = "GENERAL_ERROR";

    /**
     * Mensaje de error generico
     */
    public static final String GENERAL_ERROR_MESSAGE = "Ha ocurrido un error";

    /**
     * Objeto para dar formato a fechas
     */
    public static final String DATE_FORMAT_YYYY_MM_DD = "yyyy-MM-dd";

    /**
     * Objeto para dar formato a fechas
     */
    public static final String DATE_TIME_FORMAT_YYYY_MM_DD = "yyyy-MM-dd HH:mm:ss";
    
    /**
     * Formato utilizado para transformar las fechas del token
     */
    public static final SimpleDateFormat SIMPLE_DATE_TIME_FORMAT_TOKEN = new SimpleDateFormat("EEE MMM d HH:mm:ss z yyyy", Locale.ENGLISH);
    
    /**
     * Formato utilizado para transformar las fechas del token
     */
    public static final FastDateFormat FAST_DATE_TIME_FORMAT_TOKEN = FastDateFormat.getInstance("EEE MMM d HH:mm:ss z yyyy", Locale.ENGLISH);

    /**
     * Tamanio minimo para el nombre de tipo de telefono
     */
    public static final int MIN_SIZE_ID_NOMBRE = 2;

    /**
     * Tamanio maximo para el nombre de tipo de telefono
     */
    public static final int MAX_SIZE_ID_NOMBRE = 30;

    /**
     * Constante para identificar cadenas vacias enviadas como parametro en URI en
     * una peticion GET
     */
    public static final String EMPTY_STRING_URI = "''";

    /**
     * Tiempo de expiracion de la sesion
     */
    public static final Integer TIMEOUT_SESSION = 60;
    
    /** Tiempo de expiracion de la sesion en segundos */
    public static final Integer TIMEOUT_SESSION_IN_SECONDS = 86400;
    
    public static final String TOKEN_TYPE = "bearer";
    
    public static final String AUTHORIZATION_GRANT_TYPE_CODE = "authorization_code";
    
    public static final String AUTHORIZATION_GRANT_TYPE_REFRESH_TOKEN = "refresh_token";
    
    /**
     * Tiempo de vida minimo de un token antes de refrescarlo
     */
    public static final int TOKEN_MIN_LIFETIME = 10;
    
    /**
     * Periodo de gracia para usar el token anterior despues de un  token refresh
     */
    public static final int TOKEN_PREV_TOKEN_GRACE_PERIOD = 1;
    
    /**
     * Tiempo de expiracion de la sesion mobile
     */
    public static final Integer TIMEOUT_MOBILE_SESSION = 10080;

    /**
     * Tiempo de expiracion de la sesion publica (100 anios)
     */
    public static final Integer TIMEOUT_PUBLIC_SESSION = 52560000;

    /**
     * Identificador de los datos dentro del token
     */
    public static final String TOKEN_DATA = "TOKEN_DATA";

    /**
     * Identificador para saber el status del token
     */
    public static final String TOKEN_VALID = "TOKEN_VALID";

    /**
     * Identificador para saber el status del token
     */
    public static final String TOKEN_EXPIRED = "TOKEN_EXPIRED";

    /**
     * Identificador para saber el status del token
     */
    public static final String TOKEN_REFRESH = "TOKEN_REFRESH";

    /**
     * Identificador default para User ID Mobile Device
     */
    public static final String USER_ID_MOBILE_DEVICE = "USER_ID_MOBILE_DEVICE";

    /**
     * Identificador default para initial token
     */
    public static final String INITIAL_TOKEN = "ABCDE123456";

    /**
     * Llave para generar el token
     */
    public static final String TOKEN_KEY = "08hp4UBkjshC0CCtw+Y3/WfHUvoBrCqFqlVvlZVPpAc=";

    /**
     * Nombre del atributo de fecha de expiracion de TokenVO
     */
    public static final String EXPIRATION_DATE = "fechaExpiracion";
    
    /**
     * Nombre del atributo de fecha de creacion de TokenVO
     */
    public static final String CREATION_DATE = "fechaCreacion";

    /**
     * Nombre del atributo del idPersona
     */
    public static final String PERSONA_ID = "idPersona";
    
    /**
     * Nombre del atributo del idUsuario
     */
    public static final String USER_ID = "idUsuario";

    /**
     * Nombre del atributo de la aplicacion
     */
    public static final String APLICACION = "aplicacion";
    
    /**
     * Nombre del atributo de la aplicacion
     */
    public static final String IS_PUBLIC = "isPublic";
    
    /**
     * Nombre de los parametros de notificaciones push web
     */
    public static final String ID_ALERT = "id";
    public static final String ID_ALERT_TYPE = "idTipoAlerta";

    /**
     * Nombre del atributo de usuario dentro del token
     */
    public static final String USER_FIELD = "nombreUsuario";

    /**
     * Nombre del atributo success
     */
    public static final String SUCCESS_FIELD = "success";

    /**
     * Nombre del atributo success
     */
    public static final String NEW_TOKEN = "newToken";

    /**
     * Nombre del atributo success
     */
    public static final String NEW_TOKEN_HEADER_NAME = "New-Token";

    /**
     * Constante para autorizacion
     */
    public static final String AUTHORIZATION = "Authorization";

    /**
     * Constante que indica el nivel de profundida del stack trace para el log
     */
    public static final int CONTROLLER_LAYER_DEPTH = 6;

    /**
     * Number of objects to be created for each SmartLogger for each Class
     */
    public static final int LOGGER_INSTANCES_PER_CLASS = 2;
    
    /**
     * Number of objects to be created for each ArchitectureLogger for each Class
     */
    public static final int ARCHITECTURE_LOGGER_INSTANCES_PER_CLASS = 2;

    /**
     * Number of threads for the SmartLogger
     */
    public static final int SMART_LOGGER_THREAD_NUMBER = 2;

    /**
     * Mensaje para cuando un usuario es invlaido
     */
    public static final String INVALID_USER = "Invalid user";

    /**
     * Nombre del metodo para busquedas por id
     */
    public static final String METHOD_NAME_FIND_BY_ID = "findById";

    /**
     * Nombre del metodo para busquedas por id
     */
    public static final String METHOD_NAME_UPDATE = "update";

    /**
     * Nombre del metodo para busquedas por nombre
     */
    public static final String METHOD_NAME_FIND_BY_NAME = "findByNombre";

    /**
     * Codigo de error no asignado
     */
    public static final String DEFAULT_ERROR_CODE = "N/D";

    /**
     * Nombre del idiomaVO
     */
    public static final String IDIOMA_VO = "idiomaVO";

    /**
     * Nombre del atributo isMobile
     */
    public static final String IS_MOBILE = "isMobile";

    /**
     * Nombre del rol de administrador
     */
    public static final String ROL_NAME_ADMIN = "ADMINISTRADOR";

    /**
     * Cantidad de Kilobytes en 1 MB
     */
    public static final int MB_IN_KILOBYTES = 1024;

    /**
     * Tamanio maximo para el nombre de tipo de telefono
     */
    public static final int MAX_SIZE_ID_NOMBRE_TIPO_SUPPORT_TICKET = 50;

    /**
     * Telephone regex validation
     */
    public static final String TELEPHONE_REGEX_VALIDATION = "^[(]?[+]?(\\d{2}|\\d{3})[)]?([\\-\\s])?((\\d{12}|\\d{10}|\\d{8}|\\d{6})|(\\d{2,4}[\\-\\s]){2,6}(\\d{2,4}))$";

    /**
     * Constantes para la generaci\u00f3n de contrase\u00f1a aleatoria.
     * 
     */
    public static final int LENGTH_OF_RAMDOM_STRING_TO_CREATE = 1;
    public static final int OPTIONS_SIZE = 3;
    public static final int POSITION_ASCCI_START_LOWERCASE = 97;
    public static final int POSITION_ASCCI_START_UPPERCASE = 65;
    public static final int POSITION_ASCCI_START_SPECIAL_CHARS = 35;
    public static final int POSITION_ASCCI_END_LOWERCASE = 122;
    public static final int POSITION_ASCCI_END_UPPERCASE = 90;
    public static final int POSITION_ASCCI_END_SPECIAL_CHARS = 47;

    /**
     * Constantes para el llenado de Templates de Excel.
     * 
     */
    public static final String KEY = "id";
    public static final String GET = "get";
    public static final String SEPARADOR_HEADERS = "|";
    public static final Integer SHEET_DATA = 2;

    public static final String PARAM_INI = "[";
    public static final String PARAM_END = "]";

    public static final String SCORE = "-";
    public static final String VALIDAR_PARAMS_EXCEL = "\\[([^\\[\\]]*[^\\[\\]]*)\\]";
    public static final String EQUALS_SIGNAL = "=";

    public static final String SHEET_NAME = "sheetName";
    public static final String INIT_ROW_DATA = "initRowData";
    public static final String INIT_COL_DATA = "initColData";
    public static final String FIELD_NAMES = "fieldNames";
    public static final String DATA_LIST = "dataList";
    public static final String SEMICOLON = ";";
    public static final String SHEET_HIDDEN = "hidden";
    public static final Integer MAX_DATA = 100;

    public static final String TIPO_COMPONENT_TEMPLATE_XLS = "TEMPLATE_XLS";

    public static final String GENERIC_ERROR_CODE = "-1900";
    public static final String GENERIC_ERROR_KEY = "EJECUCION_SERVICIO";
    public static final String GENIERIC_NOT_FOUND = "No existen datos";
    
    public static final String CONFIG_GENERATE_JOBS = "CONFIG_GENERATE_JOBS";
    public static final String PARAM_URL_GENERATE_JOBS = "URL_CREATE_JOB";
    public static final String PARAM_URL_UPDATE_JOBS = "URL_UPDATE_JOB";
    public static final String PARAM_URL_STOP_JOBS = "URL_STOP_JOB";

    public static final String TARJETA_STID_DIGITAL = "TARJETA STID DIGITAL";
    public static final String TARJETA_HID_DIGITAL = "TARJETA_HID_DIGITAL";
    public static final String LAST_HOUR_24 = "23:59";

    public static final String SPACE_STRING = " ";
    
    public static final String MIDDLE_HYPHEN = "-";
    
   
    public static final String PARSE_EXCEPTION_DETAIL = " ParseException: ";
	
	// constantes de tiempo
	public static final Long HOURS_PER_DAY = 24L;
	public static final Long MINUTES_PER_HOUR = 60L;
	public static final Long SECONDS_PER_MINUTE = 60L;
	public static final Long MILISECONDS_PER_SECOND = 1000L;

    /**
     * Constructor privado para evitar instanciar clases de utileria
     */
    private GeneralConstants() {
    }

    public static final String SESION_APPLICATION = "SESION_APPLICATION";
    public static final String APPLICATION_KEY = "appKey";
    
    /**
     * TimeZone for UTC
     */
    public static final String UTC_TIME_ZONE = "UTC";
    
    /**
     * TimeZone for CDT
     */
    public static final String CDT_TIME_ZONE = "CDT";

    public static final String MEXICO_CITY_TIMEZONE = "America/Mexico_City";
    
    /**
     * Archivo con las propiedades de conexion a la nueva base 
     */
    public static final String SMART_LOGGER_DB_SQLS_CREDENTIALS_ENV_VARIABLE = "SMARTLOGGER_DB_SQLS_CREDENTIALS";
 
}
