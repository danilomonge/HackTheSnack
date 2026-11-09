package de.pecus.api.vo.subCategory;


/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  create de la case EventType
 *
 */
public class FindDetailSubCategoryResponseVO {


	// Identificador de registro
	private Long id;

	// Identificador alfanumerico
	private String name;

	private Long idCategory;
	private String nameCategory;

	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}

	public Long getIdCategory() { return this.idCategory; }
	public void setIdCategory(Long idCategory) { this.idCategory = idCategory; }

	public String getNameCategory() { return this.nameCategory; }
	public void setNameCategory(String nameCategory) { this.nameCategory = nameCategory; }
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

}

