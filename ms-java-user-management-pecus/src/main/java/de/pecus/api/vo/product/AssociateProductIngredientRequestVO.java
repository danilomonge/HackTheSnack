package de.pecus.api.vo.product;


import java.util.Date;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  create de la case Recipe
 *
 */
public class AssociateProductIngredientRequestVO {


	// Identificador alfanumerico
	private Long idProduct;

	// Descripcion del registro
	private Long idIngredient;

	// Fecha de registro
	private Date fechaRegistro;

	public Long getIdProduct() {return idProduct;}
	public void setIdProduct(Long idProduct) {this.idProduct = idProduct;}

	public Long getIdIngredient() {return idIngredient;}
	public void setIdIngredient(Long idIngredient) {this.idIngredient = idIngredient;}

	public Date getFechaRegistro() {return fechaRegistro;}
	public void setFechaRegistro(Date fechaRegistro) {this.fechaRegistro = fechaRegistro;}

}
