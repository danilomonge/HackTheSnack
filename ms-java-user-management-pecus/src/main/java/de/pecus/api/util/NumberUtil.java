package de.pecus.api.util;

import java.math.BigDecimal;
import java.text.DecimalFormat;

/**
 * Clase auxiliar para el formateo de valores decimales
 * 
 */
public final class NumberUtil {

	/**
	 * Formato decimal
	 */
	private static final DecimalFormat FORMATO_DECIMAL = new DecimalFormat("#.##");

	/**
	 * Constructor privado
	 */
	private NumberUtil() {

	}

	/**
	 * Regresa el valor a dos decimales
	 * 
	 * @param valorNdecimales
	 * @return
	 */
	public static Double getFormatoDecimal(Double valorNdecimales) {
		Double valorFormateado = null;

		if (!ValidatorUtil.isNull(valorNdecimales)) {
			valorFormateado = Double.valueOf(FORMATO_DECIMAL.format(valorNdecimales));
		}

		return valorFormateado;
	}

	public static Double stringToDouble(String valorCadena) {
		Double valor = null;

		if (!ValidatorUtil.isNullOrEmpty(valorCadena)) {
			valor = Double.valueOf(valorCadena);
		}

		return valor;
	}

	public static Long bigDecimalToLong(BigDecimal bigDecimal) {
		Long valor = null;

		if (!ValidatorUtil.isNull(bigDecimal)) {
			valor = bigDecimal.longValue();
		}

		return valor;
	}
	
	public static Integer bigDecimalToInteger(BigDecimal bigDecimal) {
		Integer valor = null;

		if (!ValidatorUtil.isNull(bigDecimal)) {
			valor = bigDecimal.intValue();
		}

		return valor;
	}
}
