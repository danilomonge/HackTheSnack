package de.pecus.api.security.services;
/**
 * Interface para los servicios de la contrasenia.
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 */
public interface PasswordService {
	/**
	 * Metodo que desencripta la contrasenia del front con el algoritmo AES.
	 * 
	 * @param cadena con la informacion para desencriptar la contrasenia.
	 * 
	 * @return contrasena en claro.
	 */
	public String decryptPasswordAES(String data);
	
	/**
	 * Metodo que encripta la contrasenia con el algoritmo SHA256.
	 * 
	 * @param cadena a encriptar.
	 * 
	 * @return contrasenia encriptada.
	 */
	public String encryptPasswordSHA256(String password);

	
}
