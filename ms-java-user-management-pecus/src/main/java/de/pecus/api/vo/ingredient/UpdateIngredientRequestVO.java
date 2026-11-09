package de.pecus.api.vo.ingredient;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo update
 *         de la case IdType
 *
 */
public class UpdateIngredientRequestVO {
	
		// id
		private Long id;
		
		// Identificador alfanumerico
		private String name;

		// Tipo de autenticacion
		private String description;

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

		public String getDescription() {
			return description;
		}

		public void setDescription(String description) {
			this.description = description;
		}
}
