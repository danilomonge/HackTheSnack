package de.pecus.api.enums;

public enum CommonHeadersEnum {

	// IDIOMA("lenguage"), LONGITUDE("longitude"), LATITUDE("latitude"), TIME_ZONE_USUARIO("time-zone-user"),
	// CODIGO_OPERACION_CLIENTE("client-operation-code"), ID_CLIENTE_INVOKE("id-client-invoke"),
	// REQUEST_DATE("request-date"), AUTHORIZATION("Authorization"), MAC_ADDRESS("mac-address");

	LANGUAGE("language"),  // Cambiado desde IDIOMA("lenguage")
    LONGITUDE("longitude"),
    LATITUDE("latitude"),
    TIME_ZONE("time-zone"),  // Cambiado desde TIME_ZONE_USUARIO("time-zone-user")
    CODIGO_OPERACION_CLIENTE("client-operation-code"), 
    ID_CLIENTE_INVOKE("id-client-invoke"),
    REQUEST_DATE("request-date"),
    AUTHORIZATION("Authorization"),
    MAC_ADDRESS("mac-address");

	String key;
	
	/**
	 * Private constructor
	 * 
	 * @param key
	 */
	private CommonHeadersEnum(String key) {
		this.key = key;
	}

	/**
	 * Get the header key
	 * 
	 * @return string with the header key
	 */
	public String getKey() {
		return key;
	}

}
