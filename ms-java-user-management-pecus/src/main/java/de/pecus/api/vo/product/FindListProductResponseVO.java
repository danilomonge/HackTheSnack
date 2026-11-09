package de.pecus.api.vo.product;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo create
 *         de la case EventType
 *
 */
public class FindListProductResponseVO {

	// id
	private Long id;
	
	// Identificador alfanumerico
	private String name;

	// Descripcion del registro
	private String descripcion;

	// Brand
	private Long idBrand;
	private String nameBrand;

	// Category
	private Long idCategory;
	private String nameCategory;

	//SubCategory
	private Long idSubCategory;
	private String nameSubCategory;


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

	public String getDescripcion() {
		return descripcion;
	}
	public void setDescripcion(String descripcion) {
		this.descripcion = descripcion;
	}

	public Long getIdBrand() {return this.idBrand;}
	public void setIdBrand(Long idBrand) {this.idBrand = idBrand;}
	public String getNameBrand() {return this.nameBrand;}
	public void setNameBrand(String nameBrand) {this.nameBrand = nameBrand;}

	public Long getIdCategory() {return this.idCategory;}
	public void setIdCategory(Long idCategory) {this.idCategory = idCategory;}
	public String getNameCategory() {return this.nameCategory;}
	public void setNameCategory(String nameCategory) {this.nameCategory = nameCategory;}

	public Long getIdSubCategory() {return this.idSubCategory;}
	public void setIdSubCategory(Long idSubCategory) {this.idSubCategory = idSubCategory;}

	public String getNameSubCategory() {return this.nameSubCategory;}
	public void setNameSubCategory(String nameSubCategory) {this.nameSubCategory = nameSubCategory;}

}
