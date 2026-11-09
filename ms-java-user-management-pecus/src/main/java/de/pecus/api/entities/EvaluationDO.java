package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;

/**
 * Catalog Recipe
 * 
 * Evaluation entity
 * @author jose.ribelles
 * @version 1.0
 * @created 24-jul.-2025 11:27:46 a. m.
 */
@Entity
@Table(name = "EVALUATION")
public class EvaluationDO extends AuditBase<Long> implements Serializable {

	private static final long serialVersionUID = -5382607608047169433L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="PK_ID")
	private Long id;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_BRAND_ID" , referencedColumnName = "PK_ID")
	private BrandDO brand;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_CATEGORY_ID" , referencedColumnName = "PK_ID")
	private CategoryDO category;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_SUBCATEGORY_ID" , referencedColumnName = "PK_ID")
	private SubCategoryDO subCategory;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_PRODUCT_ID" , referencedColumnName = "PK_ID")
	private ProductDO product;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne (fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_INGREDIENT_ID" , referencedColumnName = "PK_ID")
	private IngredientDO ingredient;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_RECIPE_ID" , referencedColumnName = "PK_ID")
	private RecipeDO recipe;

	@Column(name="DN_INGREDIENT_MEAN_PERCENTAGE")
	private Float ingredientMeanPercentage;

	@Column(name="DN_INGREDIENT_STD_PERCENTAGE")
	private Float ingredientStdPercentage;

	@Column(name="DD_EVALUATION_DATE")
	private Date evaluationDate;

	public EvaluationDO(){

	}

	public void finalize() throws Throwable {

	}

	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}

	public BrandDO getBrand() {
		return brand;
	}
	public void setBrand(BrandDO id) {
		this.brand = id;
	}

	public CategoryDO getCategory() {
		return category;
	}
	public void setCategory(CategoryDO id) {
		this.category = id;
	}

	public SubCategoryDO getSubCategory() {
		return subCategory;
	}
	public void setSubCategory(SubCategoryDO id) {
		this.subCategory = id;
	}

	public ProductDO getProduct() {
		return product;
	}
	public void setProduct(ProductDO id) {
		this.product = id;
	}

	public IngredientDO getIngredient() {
		return ingredient;
	}
	public void setIngredient(IngredientDO id) {
		this.ingredient = id;
	}

	public RecipeDO getRecipe() {
		return recipe;
	}
	public void setRecipe(RecipeDO id) {
		this.recipe = id;
	}

	public Float getIngredientMeanPercentage() { return this.ingredientMeanPercentage;}
	public void setIngredientMeanPercentage(Float ingredientMeanPercentage) {this.ingredientMeanPercentage = ingredientMeanPercentage;}

	public Float getIngredientStdPercentage() { return this.ingredientStdPercentage;}
	public void setIngredientStdPercentage(Float ingredientStdPercentage) {this.ingredientStdPercentage = ingredientStdPercentage;}

	public Date getEvaluationDate() { return this.evaluationDate;}
	public void setEvaluationDate(Date evaluationDate) {this.evaluationDate = evaluationDate;}

}