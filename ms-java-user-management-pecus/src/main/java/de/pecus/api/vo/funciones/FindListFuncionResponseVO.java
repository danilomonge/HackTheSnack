package de.pecus.api.vo.funciones;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo create
 *         de la case EventType
 *
 */
public class FindListFuncionResponseVO {

	// id
	private Long id;
	
	// Identificador alfanumerico
	private String idNombre;

	// Descripcion del registro
	private String descripcion;

	// Descripcion del registro
	private String path;
	
	private Long idAplicacion;
	
	private Boolean Checked;

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

	public String getPath() {
		return path;
	}

	public void setPath(String path) {
		this.path = path;
	}

	public Long getIdAplicacion() {
		return idAplicacion;
	}

	public void setIdAplicacion(Long idAplicacion) {
		this.idAplicacion = idAplicacion;
	}

	public Boolean getChecked() {
		return Checked;
	}

	public void setChecked(Boolean checked) {
		Checked = checked;
	}


	
}
