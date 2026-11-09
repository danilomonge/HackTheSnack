package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/

import javax.persistence.*;
import java.io.Serializable;

/**
 * Catalog Category
 * 
 * List of Categories registered in the system.
 * @author jose.ribelles
 * @version 1.0
 * @created 24-jul.-2019 11:27:46 a. m.
 */
@Entity
@Table(name = "CATEGORY")
public class CategoryDO extends AuditBase<Long> implements Serializable {

	/**
	 *
	 */
	private static final long serialVersionUID = -5382607608047169433L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="PK_ID")
	private Long id;
	@Column(name =  "DX_NAME" )
	private String name;
	@Column(name =  "DN_GENERAL_INDICATOR" )
	private Boolean generalIndicator;
	@Column(name =  "DN_MILK_INDICATOR" )
	private Boolean milkIndicator;
	@Column(name =  "DN_MEAT_INDICATOR" )
	private Boolean meatIndicator;


	public CategoryDO(){

	}

	public void finalize() throws Throwable {

	}

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

	public Boolean getGeneralIndicator() {
		return generalIndicator;
	}

	public void setGeneralIndicator(Boolean generalIndicator) {
		this.generalIndicator = generalIndicator;
	}

	public Boolean getMilkIndicator() {
		return milkIndicator;
	}

	public void setMilkIndicator(Boolean milkIndicator) {
		this.milkIndicator = milkIndicator;
	}

	public Boolean getMeatIndicator() {
		return meatIndicator;
	}

	public void setMeatIndicator(Boolean meatIndicator) {
		this.meatIndicator = meatIndicator;
	}

}