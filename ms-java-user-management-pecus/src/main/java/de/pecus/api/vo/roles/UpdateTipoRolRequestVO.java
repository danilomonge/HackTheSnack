package de.pecus.api.vo.roles;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo update
 *         de la case IdType
 *
 */
public class UpdateTipoRolRequestVO {
	
		// id
		private Long id;
		
		// Identificador alfanumerico
		private String idNombre;

		// Tipo de autenticacion
		private String descripcion;
		
		private Boolean global;

		public Long getId() {
			return id;
		}

		public void setId(Long id) {
			this.id = id;
		}

		public String getIdNombre() {
			return idNombre;
		}

		public void setIdNombre(String idNombre) {
			this.idNombre = idNombre;
		}

		public String getDescripcion() {
			return descripcion;
		}

		public void setDescripcion(String descripcion) {
			this.descripcion = descripcion;
		}

		public Boolean getGlobal() {
			return global;
		}

		public void setGlobal(Boolean global) {
			this.global = global;
		}

}
