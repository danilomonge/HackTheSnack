package de.pecus.api.vo.subCategory;


/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  create de la case EventType
 *
 */
public class CreateSubCategoryRequestVO {


	// id Category
	private Long idCategory;

	// Identificador alfanumerico
	private String name;

	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

	public Long getIdCategory() { return idCategory;}
	public void setIdCategory(Long idCategory) { this.idCategory = idCategory;}

}
