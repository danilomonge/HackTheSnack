package de.pecus.api.vo.product;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo update
 *         de la case IdType
 *
 */
public class UpdateProductRequestVO {
	
		// id
		private Long id;
		
		// Identificador alfanumerico
		private String name;

		// Tipo de autenticacion
		private String descripcion;

		// Product Id Brand
		private Long idBrand;

		// Product Id Category
		private Long idCategory;

		// Product Id Subcategory
		private Long idSubCategory;

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

		public Long getIdBrand() { return idBrand;}
		public void setIdBrand(Long idBrand) { this.idBrand = idBrand;}

		public Long getIdCategory() {return idCategory;}
		public void setIdCategory() {this.idCategory = idCategory;}

		public Long getIdSubCategory() {return idSubCategory;}
		public void setIdSubCategory() {this.idSubCategory = idSubCategory;}

}
