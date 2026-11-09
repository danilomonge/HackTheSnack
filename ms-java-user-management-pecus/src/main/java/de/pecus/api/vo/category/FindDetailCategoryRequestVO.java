package de.pecus.api.vo.category;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  findDetail de la case EventType
 *
 */
public class FindDetailCategoryRequestVO {


	// Identificador de registro
	private Long id;

	// Identificador alfanumerico
	private String name;

	// Identificador General
	private Boolean generalIndicator;

	// Identificador lacteo
	private Boolean milkIndicator;

	// Identificador carnico
	private Boolean meatIndicator;

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Boolean getGeneralIndicator() {
		return generalIndicator;
	}

	public void setGeneralIndicator(Boolean generalIndicator) {
		this.generalIndicator = generalIndicator;
	}

	public Boolean getMilkIndicator() {
		return milkIndicator;
	}

	public void setMilkIndicator(Boolean milkIndicator) {
		this.milkIndicator = milkIndicator;
	}

	public Boolean getMeatIndicator() {
		return meatIndicator;
	}

	public void setMeatIndicator(Boolean meatIndicator) {
		this.meatIndicator = meatIndicator;
	}

}
