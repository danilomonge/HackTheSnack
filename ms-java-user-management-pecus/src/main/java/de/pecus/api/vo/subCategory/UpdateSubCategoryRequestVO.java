package de.pecus.api.vo.subCategory;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo update
 *         de la case IdType
 *
 */
public class UpdateSubCategoryRequestVO {
	
		// id
		private Long id;
		// Identificador alfanumerico
		private String name;
		// Category
		private Long	idCategory;

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

		public Long getIdCategory() {return idCategory;}
		public void setIdCategory(Long idCategory) {this.idCategory = idCategory;}

}
