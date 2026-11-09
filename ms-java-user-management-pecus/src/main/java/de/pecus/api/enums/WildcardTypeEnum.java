package de.pecus.api.enums;

/**
 * Enum created to create the SQL LIKE statements dinamically according to the desired
 * wildcard position
 * 
 * Example:
 * Right = "Some Text%"
 * LEFT = "%Some Text"
 * BOTH_SIDES = "%Some Text%"
 * NONE = "Some Text"
 * 
 * @author Juan Carlos Contreras Vazquez
 */
public enum WildcardTypeEnum {
	
	RIGHT, LEFT, BOTH_SIDES, NONE;
}