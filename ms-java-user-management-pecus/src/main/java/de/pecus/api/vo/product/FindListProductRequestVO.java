package de.pecus.api.vo.product;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  findDetail de la case EventType
 *
 */
public class FindListProductRequestVO {

	private String name;
	private Integer idBrand;
	private Integer idCategory;

	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

	public Integer getIdBrand() {return this.idBrand;}
	public Integer getIdCategory() {return this.idCategory;}
	public void setIdBrand(Integer idBrand) {this.idBrand = idBrand;}
	public void setIdCategory(Integer idCategory) {this.idCategory = idCategory;}

}
