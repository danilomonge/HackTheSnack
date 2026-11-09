package de.pecus.api.vo.category;


/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  create de la case EventType
 *
 */
public class CreateCategoryRequestVO {


	// Identificador alfanumerico
	private String name;

	// Indicador general
	private Boolean generalIndicator;

	// Indicador lacteo
	private Boolean milkIndicator;

	// Indicador carne
	private Boolean meatIndicator;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Boolean isGeneralIndicator() {
		return generalIndicator;
	}

	public void setGeneralIndicator(Boolean generalIndicator) {
		this.generalIndicator = generalIndicator;
	}

	public Boolean isMilkIndicator() {
		return milkIndicator;
	}

	public void setMilkIndicator(Boolean milkIndicator) {
		this.milkIndicator = milkIndicator;
	}

	public Boolean isMeatIndicator() {
		return meatIndicator;
	}

	public void setMeatIndicator(Boolean meatIndicator) {
		this.meatIndicator = meatIndicator;
	}

}
