package de.pecus.api.security.services.impl;

import java.util.Base64;

import org.springframework.stereotype.Service;

import de.pecus.api.security.services.PasswordService;
import de.pecus.api.util.CryptoUtil;
/**
 * Clase para los servicios de la contrase&ntilde;a.
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 */
@Service
public class PasswordServiceImpl implements PasswordService {

	public static final String ENCRYPT_KEY = "p3cu5";
	
	/**
	 * Metodo que usa la utileria de criptografia para desencriptar la contrase&ntilde;a.
	 * 
	 * @param password cadena de la contrase&ntilde;a.
	 * 
	 * @return contrase&ntilde;a encriptada.
	 */
	@Override
	public String decryptPasswordAES(String password) {
		if(password != null){
			String decodedPassword =  new String(Base64.getDecoder().decode(password));
			if(decodedPassword.split("::").length == 3) {
				return new CryptoUtil().decrypt(decodedPassword.split("::")[1], decodedPassword.split("::")[0], ENCRYPT_KEY, decodedPassword.split("::")[2]);
			}
		}
		return null;
	}

	/**
	 * Metodo que encripta la contrase&ntilde;a con el algoritmo SHA256.
	 * 
	 * @param password cadena para encriptar.
	 * 
	 * @return contrase&ntilde;a encriptada.
	 */
	@Override
	public String encryptPasswordSHA256(String password) {
		if(password != null) {
			return new CryptoUtil().digest(password, "SHA-256");
		}
		return null;
	}
	
	
}
