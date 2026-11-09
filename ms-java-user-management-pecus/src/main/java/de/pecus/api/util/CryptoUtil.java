package de.pecus.api.util;

import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Arrays;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Base64;
import org.apache.commons.codec.binary.Hex;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import de.pecus.api.encryption.util.EncryptionUtil;

/**
 * Utiler&iacute;a para encriptar y desencriptar cadenas por medio de diferentes protocolos de encripci&oacute;n.
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public final class CryptoUtil {
    
    private static final Logger LOG = LoggerFactory.getLogger( CryptoUtil.class );
    
    private static final String COLON = ":";
    
    /** Llave hexadecimal de encripci&oacute;n */
    private final String hexadecimalKey;
    
    /** Protocolo de encripci&oacute;n AES */
    public static final String AES = "AES";
    
    /** Protocolo de cifrado SHA-1 */
    public static final String SHA1 = "SHA-1";
    
    /** Protocolo de cifrado MD5 */
    public static final String MD5 = "MD5";
    
    /*******************************************************************************/
    /******************* PARA GENERACION DE CODIGOS EN INVITACIONES ****************/
    private static final String ALGORITHM = "md5";
    private static final String DIGEST_STRING = "HG58YZ3CR9";
    private static final String CHARSET_UTF_8 = "utf-8";
    private static final String SECRET_KEY_ALGORITHM = "DESede";
    private static final String TRANSFORMATION_PADDING = "DESede/CBC/PKCS5Padding";
    private static final char[] HEX_ARRAY = "0123456789ABCDEF".toCharArray();
    /*******************************************************************************/

    public static final int DEFAULT_SALT_BYTE_SIZE = 16;
    
    public static final int DEFAULT_HASH_BYTE_SIZE = 16;
    
    public static final int DEFAULT_PBKDF2_ITERATIONS = 1000;

    public static final int ITERATION_INDEX = 0;
    
    public static final int PBKDF2_INDEX = 1;
    
    public static final int KEY_SIZE = 128;
    
    public static final int ITERATION_COUNT = 1000;
    
    // Salt
    private static final byte[] SALT = { (byte) 0xc7, (byte) 0x73, (byte) 0x21, (byte) 0x8c, (byte) 0x7e, (byte) 0xc8,
            (byte) 0xee, (byte) 0x99 };

    /**
     * Constructor default
     */
    public CryptoUtil() {
        // La llave debe ser de 128 bits (long 32 hexadecimales)
        String digested = "B9DA93BD5C5B3CBFCF0AC5BC198E773A";
        this.hexadecimalKey = saltHexadecimalKey( digested );
    }

    /**
     * Constructor que recibe la frase de encripci&oacute;n inicial
     * 
     * @param phrase
     */
    public CryptoUtil( String phrase ) {
        // La llave debe ser de 128 bits (long 32 hexadecimales)
        String digested = this.digest( phrase, CryptoUtil.SHA1 ).substring( 0, 32 );
        this.hexadecimalKey = saltHexadecimalKey( digested );
    }

    /**
     * Metodo para desencriptar una Cadena
     * 
     * @param encryptedText Cadena a desencriptar
     * @return El texto desencriptado
     * @throws NoSuchAlgorithmException
     * @throws NoSuchPaddingException
     * @throws InvalidKeyException
     * @throws IllegalBlockSizeException
     * @throws BadPaddingException
     */
    public String decrypt( String encryptedText ) {
        SecretKeySpec sks = getSecretKeySpec();
        Cipher cipher;
        byte[] decrypted = null;
        try{
            cipher = Cipher.getInstance( CryptoUtil.AES );
            cipher.init( Cipher.DECRYPT_MODE, sks );
            decrypted = cipher.doFinal( hexStringToByteArray( encryptedText ) );
        }
        catch( NoSuchAlgorithmException | NoSuchPaddingException  | InvalidKeyException  | IllegalBlockSizeException  | BadPaddingException e ){
            LOG.error( e.getMessage(), e );
        }

        return decrypted != null ? new String( decrypted ) : encryptedText;
    }

    /**
     * Metodo para encriptar una Cadena
     * 
     * @param value Cadena a encriptar
     * @return cadena encriptada
     * @throws NoSuchAlgorithmException
     * @throws NoSuchPaddingException
     * @throws InvalidKeyException
     * @throws InvalidAlgorithmParameterException
     * @throws IllegalBlockSizeException
     * @throws BadPaddingException
     */
    public String encrypt( String value ) {
        SecretKeySpec sks = getSecretKeySpec();

        byte[] encrypted = null;
        try{
            Cipher cipher = Cipher.getInstance( CryptoUtil.AES );
            cipher.init( Cipher.ENCRYPT_MODE, sks, cipher.getParameters() );
            encrypted = cipher.doFinal( value.getBytes() );
        }
        catch( NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException | InvalidAlgorithmParameterException | IllegalBlockSizeException | BadPaddingException e ){
            LOG.error( e.getMessage(), e );
        }

        return encrypted != null ? byteArrayToHexString( encrypted ) : value;

    }

    /***
     * Encripta un mensaje de texto mediante algoritmo de resumen de mensaje.
     * 
     * @param message texto a encriptar
     * @param algorithm algoritmo de encripcion, puede ser: MD5, SHA-1
     * @return mensaje encriptado
     */
    public String digest( String message, String algorithm ) {
        byte[] digest = null;
        byte[] buffer = message.getBytes();
        MessageDigest messageDigest;
        try{
            messageDigest = MessageDigest.getInstance( algorithm );
            messageDigest.reset();
            messageDigest.update( buffer );
            digest = messageDigest.digest();
        }
        catch( NoSuchAlgorithmException e ){
            LOG.error( e.getMessage(), e );
        }
        return digest != null ? byteArrayToHexString( digest ) : "";

    }

    /**
     * Convierte el arreglo de bytes a su representaci&oacute;n hexadecimal
     * 
     * @param b arreglo de bytes
     * @return Representaci&oacute;n hexadecimal
     */
    public static String byteArrayToHexString( byte[] b ) {
        StringBuilder sb = new StringBuilder( b.length * 2 );
        for( int i = 0; i < b.length; i++ ){
            int v = b[i] & 0xff;
            if( v < 16 ){
                sb.append( '0' );
            }
            sb.append( Integer.toHexString( v ) );
        }
        return sb.toString();
    }

    /**
     * Convierte una cadena de hexadecimales a su representaci&oacute;n en un arreglo de bytes
     * 
     * @param s cadena hexadecimal
     * @return arreglo de bytes
     */
    public static byte[] hexStringToByteArray( String s ) {
        byte[] b = new byte[s.length() / 2];
        for( int i = 0; i < b.length; i++ ){
            int index = i * 2;
            int v = Integer.parseInt( s.substring( index, index + 2 ), 16 );
            b[i] = (byte) v;
        }
        return b;
    }

    /**
     * Obtiene la llave secreta de encripci&oacute;n
     * 
     * @return llave secreta
     */
    private SecretKeySpec getSecretKeySpec() {
        byte[] keyEncoded = hexStringToByteArray( hexadecimalKey );

        return new SecretKeySpec( keyEncoded, CryptoUtil.AES );
    }

    /**
     * Aplica un "salting" a la frase codificada
     * 
     * @param digested
     * @return la llave "salteada"
     */
    private String saltHexadecimalKey( String digested ) {
        byte[] key = CryptoUtil.hexStringToByteArray( digested );
        for( int i = 0; i < 20; i++ ){
            for( int j = 0; j < key.length; j++ ){
                int k = (j + i) % SALT.length;
                key[j] = (byte) (key[j] ^ SALT[k]);
            }
        }
        return CryptoUtil.byteArrayToHexString( key );
    }

    /**
     * Crea una hash a partir de una contrase&ntilde;a y un salteo
     * 
     * @param password
     * @param salt
     * @return
     * @throws NoSuchAlgorithmException
     * @throws InvalidKeySpecException
     */
    public static String createHash( String password, byte[] salt ) throws NoSuchAlgorithmException,
            InvalidKeySpecException {
        return createHash( password.toCharArray(), salt, DEFAULT_HASH_BYTE_SIZE );
    }

    /**
     * Returns a salted PBKDF2 hash of the password.
     * 
     * @param password the password to hash
     * @return a salted PBKDF2 hash of the password
     */
    public static String createHash( String password, byte[] salt, int hashByteSize ) throws NoSuchAlgorithmException,
            InvalidKeySpecException {
        return createHash( password.toCharArray(), salt, hashByteSize );
    }

    /**
     * Returns a salted PBKDF2 hash of the password.
     * 
     * @param password the password to hash
     * @return a salted PBKDF2 hash of the password
     */
    private static String createHash( char[] password, byte[] salt, int hashByteSize ) throws NoSuchAlgorithmException,
            InvalidKeySpecException {
        // Hash the password
        byte[] hash = PasswordHash.pbkdf2( password, salt, DEFAULT_PBKDF2_ITERATIONS,
            hashByteSize <= 0 ? DEFAULT_HASH_BYTE_SIZE : hashByteSize );
        // format iterations:hash
        return StringUtil.buildStringUsingMutable( DEFAULT_PBKDF2_ITERATIONS, COLON, byteArrayToHexString( hash ) );
    }

    /**
     * Validates a password using a hash.
     * 
     * @param password the password to check
     * @param correctHash the hash of the valid password
     * @return true if the password is correct, false if not
     */
    public static boolean validatePassword( String password, String correctHash, byte[] correctSalt )
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        return validatePassword( password.toCharArray(), correctHash, correctSalt );
    }

    /**
     * Validates a password using a hash.
     * 
     * @param password the password to check
     * @param correctHash the hash of the valid password
     * @return true if the password is correct, false if not
     */
    public static boolean validatePassword( char[] password, String correctHash, byte[] correctSalt )
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        // Decode the hash into its parameters
        String[] params = correctHash.split( COLON );
        int iterations = Integer.parseInt( params[ITERATION_INDEX] );
        byte[] hash = hexStringToByteArray( params[PBKDF2_INDEX] );
        // Compute the hash of the provided password, using the same salt,
        // iteration count, and hash length
        byte[] testHash = PasswordHash.pbkdf2( password, correctSalt, iterations, hash.length );
        // Compare the hashes in constant time. The password is correct if
        // both hashes match.
        return PasswordHash.slowEquals( hash, testHash );
    }

    /**
     * Genera un arreglo de bytes (salteo) pseudoaleatorio
     * 
     * @return
     */
    public static byte[] generateSalt() {
        return generateSalt( DEFAULT_SALT_BYTE_SIZE );

    }

    /**
     * Genera un arreglo de bytes (salteo) pseudoaleatorio de la longitud indicada
     * 
     * @param saltByteSize
     * @return
     */
    public static byte[] generateSalt( int saltByteSize ) {
        // Generate a random salt
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[saltByteSize <= 0 ? DEFAULT_SALT_BYTE_SIZE : saltByteSize];
        random.nextBytes( salt );
        return salt;
    }

    /**
     * Metodo para la desencripcion para el texto.
     * 
     * @param salt salt.
     * @param iv vector de inicializacion.
     * @param passphrase frase de encripcion.
     * @param ciphertext cadena a desencriptar.
     * @return cadena desencriptada.
     */
    public String decrypt(String salt, String iv, String passphrase, String ciphertext) {
        try {
            SecretKey key = generateKey(salt, passphrase);
            byte[] decrypted = doFinal(Cipher.DECRYPT_MODE, key, iv, base64(ciphertext));
            return new String(decrypted, StandardCharsets.UTF_8);
        }catch (Exception e){
            return null;
        }
    }

    /**
     * Metodo para inicializar el cipher con el vector de inicializacion.
     * 
     * @param encryptMode modo de encripcion.
     * @param key llave de encripcion.
     * @param iv cadena del vector de inicializacion.
     * @param arreglo de byte de la cadena.
     * @return arreglo de bytes.
     */
    private byte[] doFinal(int encryptMode, SecretKey key, String iv, byte[] bytes) {
        try {
        	Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(encryptMode, key, new IvParameterSpec(hex(iv)));
            return cipher.doFinal(bytes);
        } catch (InvalidKeyException
                | InvalidAlgorithmParameterException
                | IllegalBlockSizeException
                | BadPaddingException
                | NoSuchAlgorithmException 
                | NoSuchPaddingException e) {
            return new byte[5];
        }
    }

    /**
     * Metodo para generar la llave de encripcion.
     * 
     * @param salt cadena salt.
     * @param passphrase frase de encripcion.
     * @return la llave secreta.
     */
    private SecretKey generateKey(String salt, String passphrase) {
        try {
            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
            KeySpec spec = new PBEKeySpec(passphrase.toCharArray(), hex(salt), ITERATION_COUNT, KEY_SIZE);
            return new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
        }
        catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            return null;
        }
    }

    /**
     * Metodo para convertir una cadena en arreglo de bytes con decode base64.
     * 
     * @param str cadena a convertir
     * @return arreglo byte
     */
    public static byte[] base64(String str) {
        return Base64.decodeBase64(str);
    }

    /**
     * Metodo para convertir una cadena en arreglo de bytes con decode hexadecimal.
     * 
     * @param str cadena a convertir
     * @return arreglo de byte
     */
    public static byte[] hex(String str) {
        try {
            return Hex.decodeHex(str.toCharArray());
        }
        catch (DecoderException e) {
            throw new IllegalStateException(e);
        }
    }
	
    
    /**
     * Metodo para encriptar una cadena con un algoritmo MD5
     *
     * @param message the message
     * @return the byte[]
     * @throws Exception the exception
     */
	public static byte[] encryptMd5(String message) {
		byte[] cipherText = null;
		try {
			final MessageDigest md = MessageDigest.getInstance(ALGORITHM);
			final byte[] digestOfPassword = md.digest(DIGEST_STRING.getBytes(CHARSET_UTF_8));
			final byte[] keyBytes = Arrays.copyOf(digestOfPassword, 24);
			for (int j = 0, k = 16; j < 8;) {
				keyBytes[k++] = keyBytes[j++];
			}

			final SecretKey key = new SecretKeySpec(keyBytes, SECRET_KEY_ALGORITHM);
			final IvParameterSpec iv = new IvParameterSpec(new byte[8]);
			final Cipher cipher = Cipher.getInstance(TRANSFORMATION_PADDING);
			cipher.init(Cipher.ENCRYPT_MODE, key, iv);

			final byte[] plainTextBytes = message.getBytes(CHARSET_UTF_8);
			cipherText = cipher.doFinal(plainTextBytes);

		} catch (Exception e) {
			LOG.error(e.getMessage(), e);
		}

		return cipherText;
	} 
	
  
    /**
     * Metodo para desencriptar una cadena encriptada con un algoritmo MD5
     *
     * @param message the message
     * @return the string
     * @throws Exception the exception
     */
    public static String decryptMd5(byte[]  message) { 
    	String decipherText = null;
    	try {
    		final MessageDigest md = MessageDigest.getInstance(ALGORITHM); 
    		final byte[] digestOfPassword = md.digest(DIGEST_STRING.getBytes(CHARSET_UTF_8)); 
    		final byte[] keyBytes = Arrays.copyOf(digestOfPassword, 24); 
    		for (int j = 0, k = 16; j < 8;) { 
    			keyBytes[k++] = keyBytes[j++]; 
    		} 
    		
    		final SecretKey key = new SecretKeySpec(keyBytes, SECRET_KEY_ALGORITHM); 
    		final IvParameterSpec iv = new IvParameterSpec(new byte[8]); 
    		final Cipher decipher = Cipher.getInstance(TRANSFORMATION_PADDING); 
    		decipher.init(Cipher.DECRYPT_MODE, key, iv); 
    		
    		final byte[] plainText = decipher.doFinal(message); 
    		
    		decipherText = new String(plainText, CHARSET_UTF_8); 
			
		} catch (Exception e) {
			LOG.error(e.getMessage(), e);
		}
    	
    	return decipherText;
    }
    
    
    /**
     * Metodo para encriptar una cadena con un algoritmo base64 con una llave para Genexus
     *
	 * @param message
	 * @param key
	 * @return
	 */
	public static String encryptBase64Gnexus(String message, String key) {
		String encryptString = null;
		try {
		
		encryptString = EncryptionUtil.encrypt64(message, key);		
		} catch (Exception e) {
			LOG.error(e.getMessage(), e);
			encryptString = null;
		}
		
		return encryptString;
	} 
	
	
    /**
     * Metodo para encriptar una cadena con un algoritmo base64 con una llave para Genexus
     *
	 * @param message
	 * @param key
	 * @return
	 */
	public static String decryptBase64Gnexus(String message, String key) {
		String text = null;
		try {
		
		text = EncryptionUtil.decrypt64(message, key);		
		} catch (Exception e) {
			LOG.error(e.getMessage(), e);
			text = null;
		}
		
		return text;
	} 
    
	/**
	 * Metodo para convertir un arreglo de bytes a una cadena en hexadecimal
	 *
	 * @param bytes the bytes
	 * @return the string
	 */
	public static String bytesToHex(byte[] bytes) {
	    char[] hexChars = new char[bytes.length * 2];
	    for (int j = 0; j < bytes.length; j++) {
	        int v = bytes[j] & 0xFF;
	        hexChars[j * 2] = HEX_ARRAY[v >>> 4];
	        hexChars[j * 2 + 1] = HEX_ARRAY[v & 0x0F];
	    }
	    return new String(hexChars);
	}
}
