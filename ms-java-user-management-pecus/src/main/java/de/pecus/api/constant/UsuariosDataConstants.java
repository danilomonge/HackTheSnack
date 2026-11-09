package de.pecus.api.constant;

/**
 * Clase de constantes
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public final class UsuariosDataConstants {
	
	/**
	 * Tamanno minimo para el atributo idNombre
	 */
	public static final int MIN_SIZE_ID_NOMBRE = 2;


	/**
	 * Tamanno maximo para el atributo Id_Nombre
	 */
	public static final int MAX_SIZE_ID_NOMBRE = 20;
	
	/**
	 * Tamanno minimo para el atributo Descripcion
	 */
	public static final int MIN_SIZE_DESCRIPCION = 2;


	/**
	 * Tamanno maximo para el atributo Descripcion
	 */
	public static final int MAX_SIZE_DESCRIPCION = 100;

	/**
	 * Tama\u00f1o minimo requerido para la contrase\u00f1a de usuario.
	 */
	public static final int MIN_SIZE_PASSWORD = 6;

	/**
     * Nombre del metodo para busquedas por nombre de anuncio
     */
	public static final String METHOD_NAME_FIND_BY_NAME = "findByName";

	/**
	 * Nombre del parametro a enviar al modulo Notificaciones
	 */
	public static final String CODIGO = "codigo";

	/**
	 * Nombre del tipo de notificacion que se enviara al modulo Notificaciones
	 */
	public static final String CODIGO_ACTIVACION_ADMIN_CONDO = "CODIGO_ACTIVACION_ADMIN_CONDO";

	/**
	 * Nombre del tipo de notificacion que se enviara al modulo Notificaciones
	 */
	public static final String REGISTRO_ADMIN_CONDO_EXITOSO = "REGISTRO_ADMIN_CONDO_EXITOSO";
	
	/**
	 * Nombre del tipo de notificacion que se enviara al modulo Notificaciones
	 */
	public static final String ENVIO_CONTRA_RAMDON_USUARIO = "ENVIO_CONTRA_USUARIO_EMPLEADO";
	
	/**
	 * Nombre del tipo de notificacion que se enviara al modulo Notificaciones
	 */
	public static final String NOTIFICACION_REGISTRO_MOBILE_EXITOSO = "NOTIFICACION_REGISTRO_MOBILE_EXITOSO";
	
	/**
	 * Nombre unico del tipo de contrato de version de prueba
	 * 
	 */
	public static final String PAQUETE_SERVICIO_FREEMIUM = "FREE";
	
	/**
	 * Parametro - nombre - que se insertara en la plantilla.
	 * 
	 */
	public static final String PARAMETRO_PLANTILLA_NOMBRE = "nombre";
	
	/**
	 * Parametro - correo - que se insertara en la plantilla
	 * 
	 */
	public static final String PARAMETRO_PLANTILLA_CORREO = "correo";


	/**
	 * Parametro - contrasena - que se insertara en la plantilla de notificacion de creacion de usuario para el registro del empleado
	 * 
	 */
	public static final String PARAMETRO_PLANTILLA_PASSWORD = "contrasena";

	/**
	 * Numero para setear un tipo de catalogo por defecto.
	 *
	 */
	public static final Long DEFAULT_NUMBER_ONE = 1L;
	
	/**
	 * Parametro - correo - que se insertara en la plantilla
	 * 
	 */
	public static final String FORMATO_REPORTE_PDF = "PDF";
	
	/**
	 * Parametro - correo - que se insertara en la plantilla
	 * 
	 */
	public static final String REPORTE_USUARIO_INACTIVO = "REPORTE_USUARIO_INACTIVO";
	
	/**
	 * Parametro - correo - que se insertara en la plantilla
	 * 
	 */
	public static final String ID_REPORTE_USUARIO_INACTIVO = "REPORTE_USUARIO_INACTIVO";
	
	/**
	 * Estatus para cambio de password
	 * 
	 */
	public static final int ESTATUS_CAMBIO_PASSWORD = 0;
	
	/**
	 * Estatus de password actualizado
	 * 
	 */
	public static final int ESTATUS_PASSWORD_ACTUALIZADO = 1;
	
	/**
	 * Codigo de activacion inactivo
	 */
	public static final String CODIGO_ACTIVACION_INACTIVO = "0";
	
	public static final int ALEXA_CODE_SIZE = 10;
	
	public static final int PHONE_NUMBER_SIZE = 12;
	
	public static final Long DEFAULT_ADDRESS_TYPE = 1L;
	
	public static final String DEFAULT_ID_NOMBRE_DOMICILIO = "Domicilio de ";
	
	public static final String LADA_MEXICO = "+52";
	
	public static final String APEX_EMAIL_CONTACT_TYPE = "email";
	
	public static final String APEX_PHONE_CONTACT_TYPE = "phone";

	public static final int REQUEST_MLPERSON_TYPE_PERSON = 2;

	public static final int REQUEST_MLPERSON_PRIVACY = 1;
	
	/**
	 * Nombre de la plantilla de notificacion para reseteo de password por canal EMAIL
	 */
	public static final String NOTIFICACION_EMAIL_RESET_PASSWORD = "NOTIFICACION_EMAIL_RESET_PASSWORD";

	public static final String CODIGO_ACTIVACION = "CODIGO_ACTIVACION";
	
	public static final String NOMBRE_ROL_MEDICO = "MEDICO";

	/**
	 * Nombre de la plantilla de notificacion para reseteo de password por canal EMAIL
	 */
	public static final String NOTIFICACION_EMAIL_BIENVENIDA = "BIENVENIDA_APP";
	
	public static final String NOMBRE_ROL_PACIENTE = "PACIENTE";
	
	/**
	 * Nombre de la plantilla de notificacion para reseteo de password por canal PUSH
	 */
	public static final String NOTIFICACION_PUSH_RESET_PASSWORD = "NOTIFICACION_PUSH_RESET_PASSWORD";
	
	/**
	 * Constructor privado para evitar instanciar clases de utileria
	 */
	private UsuariosDataConstants() {
	}

	/*
	 * Tiempo de vida del codigo de activacion
	 */
	public static final int CODIGO_ACTIVACION_LIFETIME = 5;

	public static final int CODIGO_ACTIVACION_INTENTOS_LIMITE = 5;
	
	public static final String AUTHENTICATION_TYPE_AZURE_AD = "AZUREAD";
	
	public static final String AUTHENTICATION_TYPE_DBUSUARIOSEG = "DBUSUARIOSEG";
	
	public static final String NOTIFICACION_EMAIL_BIENVENIDA_AS = "AS_BIENVENIDA_APP";

	public static final String WELCOME_USER_FROM_APEX = "WELCOME_USER_FROM_APEX";

	public static final String PARAMETRO_PLANTILLA_EMAIL_USER = "userName";

	public static final String PARAMETRO_PLANTILLA_EMAIL_CODE = "codigoActivacion";

	public static final String NOTIFICACION_AS_EMAIL_RESET_PASSWORD = "NOTIFICACION_AS_EMAIL_RESET_PASSWORD";
	
	public static final String NOTIFICACION_AS_CODIGO_ACTIVACION = "AS_CODIGO_ACTIVACION";
	
	public static final String SMS_CODIGO_ACTIVACION = "SU CODÍGO DE ACTIVACIÓN ES: ";
	
	public static final Boolean DONT_SAVE = false;
	
	public static final Boolean SAVE = true;

	public static final String ALTA_USUARIO_POS = "ALTA_USUARIO_POS";

	public static final String ALTA_USUARIO_POS_ERROR = "ALTA_USUARIO_POS_ERROR";

	public static final Integer ALTA_POS_ID_COMPONENTE = 4;

	public static final Integer ALTA_POS_ID_TIPO_COMPONENTE = 4;


}
