package de.pecus.api.util;

import java.util.Date;
import java.util.List;

import de.pecus.api.enums.WildcardTypeEnum;

/**
 * Helper class to create criteria queries
 * 
 * @author carlos
 */
public final class CriteriaUtil {
	
	private static final String WILDCARD = "%";
	
	/**
	 * Private constructor to disable default constructor
	 */
	private CriteriaUtil() {
		
	}
	
	public static String validateNullLike(String parameterToEvaluate, WildcardTypeEnum wildcardTypeEnum) {
		String parameter = null;
		if(!ValidatorUtil.isNullOrEmpty(parameterToEvaluate)) {
			if(WildcardTypeEnum.RIGHT.equals(wildcardTypeEnum)) {
	    	    parameter = parameterToEvaluate + WILDCARD;
			} else if(WildcardTypeEnum.LEFT.equals(wildcardTypeEnum)) {
				parameter = WILDCARD + parameterToEvaluate;
			} else if(WildcardTypeEnum.BOTH_SIDES.equals(wildcardTypeEnum)) {
				parameter = WILDCARD + parameterToEvaluate + WILDCARD;
			} else {
				parameter = parameterToEvaluate;
			}
	    }
		return parameter;
	}
	
	public static Long validateNull(Long parameterToEvaluate) {
		Long parameter = null;
		if(!ValidatorUtil.isNullOrZero(parameterToEvaluate)) {
			parameter = parameterToEvaluate;
	    }
		return parameter;
	}
	
	public static Integer validateNull(Integer parameterToEvaluate) {
		Integer parameter = null;
		if(!ValidatorUtil.isNullOrZero(parameterToEvaluate)) {
			parameter = parameterToEvaluate;
	    }
		return parameter;
	}
	
	public static Double validateNull(Double parameterToEvaluate) {
		Double parameter = null;
		if(!ValidatorUtil.isNullOrZero(parameterToEvaluate)) {
			parameter = parameterToEvaluate;
	    }
		return parameter;
	}
	
	public static Date validateNull(Date parameterToEvaluate) {
        Date parameter = null;
        if(!ValidatorUtil.isNull(parameterToEvaluate)) {
            parameter = parameterToEvaluate;
        }
        return parameter;
    }

	public static <T> List<T> validateNullOrEmpty(List<T> parameterToEvaluate) {
		List<T> parameter = null;
		if (!ValidatorUtil.isNullOrEmpty(parameterToEvaluate)) {
			parameter = parameterToEvaluate;
		}
		return parameter;
	}
	
}