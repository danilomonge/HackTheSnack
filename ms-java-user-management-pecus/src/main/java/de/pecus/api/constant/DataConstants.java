package de.pecus.api.constant;

/**
 * Constants class
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public final class DataConstants {

    /**
     * Maximum size for the attribute Id_Nombre
     */
    public static final int MAX_SIZE_ID_NOMBRE = 20;

    /**
     * Maximum size for the attribute Descripcion
     */
    public static final int MAX_SIZE_DESCRIPCION = 100;

    /**
     * Maximum size for the attribute numero
     */
    public static final int MAX_SIZE_NUMERO = 10;

    /**
     * Maximum size for the attribute region
     */
    public static final int MAX_SIZE_REGION = 5;
    
    /**
     * Environment variable containing the key 
     * required for sending emails.
     */
    public static final String SENDGRID_API_KEY_ENV_VAR = "SENDGRID_API_KEY";
    
    public static final String REGISTRO_ADMIN_CONDO_EXITOSO = "REGISTRO_ADMIN_CONDO_EXITOSO";
    
    public static final String IMAGE_PECUS = "https://admin.pecus.com.mx/pecus-admin/assets/images/mailings/isotipo.png";
    
    public static final String BADGE_PECUS = "https://admin.pecus.com.mx/pecus-admin/assets/images/mailings/isotipo.png";
    
    public static final String ICON_PECUS = "https://admin.pecus.com.mx/pecus-admin/assets/images/mailings/pecuslogoazul.png";
    
    public static final String DEFAULT_TAG = "DEFAULT_TAG";

    /**
     * Private constructor to prevent instantiation of utility classes
     */
    private DataConstants() {
    }

}

