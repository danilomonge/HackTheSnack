package de.pecus.api.vo.subCategory;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  findDetail de la case EventType
 *
 */
public class FindListSubCategoryRequestVO {

	private String name;
	private Integer idCategory;

	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

	public Integer getIdCategory() {return idCategory;}
	public void setIdCategory(Integer idCategory) {this.idCategory = idCategory;}

}
