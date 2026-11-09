package de.pecus.api.util;

import java.util.ArrayList;
import java.util.List;

import de.pecus.api.constant.GeneralConstants;


/**
 * Clase de utileria para listas
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 */
public class ListUtil {
	
    /**
     * Valida si la lista es nula o esta vacia
     * 
     * @param list Lista a validar
     * 
     * @return true si es nula o esta vacia
     */
    public static boolean isEmpty(List<?> list) {
		return list == null || list.isEmpty();
	}
	
	
	/**
	 * Regresa el tamanio de la lista
	 * 
	 * @param list Lista a validar
	 * 
	 * @return Tamanio de la lista o cero si es nula o esta vacia
	 */
	public static <T> Integer getGenericTotalSize (List<T> list)  {
		return list != null ? list.size() : GeneralConstants.ZERO;
	}
	
	
	
	/**
	 * Regresa el total de la lista.
	 * @param listValidate
	 * @return
	 */
	@SuppressWarnings("rawtypes")
	public List getGenericSimpleList (List listValidate) {
		return listValidate != null && !listValidate.isEmpty() ? listValidate : new ArrayList();
	}
	
	public static <T> T getLast(List<T> list) {
		return ValidatorUtil.isNullOrEmpty(list) ? null : list.get(list.size() -1);
	}
	
	public static <T> T getFirst(List<T> list) {
		return ValidatorUtil.isNullOrEmpty(list) ? null : list.get(GeneralConstants.ZERO);
	}

}
