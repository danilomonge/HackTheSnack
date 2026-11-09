package de.pecus.api.vo.evaluation;


import java.util.Date;
import java.util.List;

/**
 * 
 * @author Emilio Ribelles
 *
 * Data output for a single evaluation
 *
 */
public class FindDetailEvaluationResponseVO {


	// Identificador de registro
	private Long id;

	// Brand Data
	private Long idBrand;
	private String brandName;

	// Category Data
	private Long idCategory;
	private String categoryName;

	//SubCategory Data
	private Long idSubCategory;
	private String subCategoryName;

	// Product Data
	private Long idProduct;
	private String productName;

	// Ingredient Data
	private Long idIngredient;
	private String ingredientName;

	// Recipe Data
	private Long idRecipe;

	// Evaluation Date
	private Date evaluationDate;

	// Ingredient mean precentaje
	private Float ingredientMeanPercentage;

	// Ingredient variation precentaje
	private Float ingredientStdPercentage;

	//List of results
	private List<ResultItemVO> resultList;

	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}

	public Long getIdBrand() {return idBrand;}
	public void setIdBrand(Long idBrand) {this.idBrand = idBrand;}
	public String getBrandName() {return brandName;}
	public void setBrandName(String brandName) {this.brandName = brandName;}

	public Long getIdCategory() {return idCategory;}
	public void setIdCategory(Long idCategory) {this.idCategory = idCategory;}
	public String getCategoryName() {return categoryName;}
	public void setCategoryName(String categoryName) {this.categoryName = categoryName;}

	public Long getIdSubCategory() {return idSubCategory;}
	public void setIdSubCategory(Long idSubCategory) {this.idSubCategory = idSubCategory;}
	public String getSubCategoryName() {return subCategoryName;}
	public void setSubCategoryName(String subCategoryName) {this.subCategoryName = subCategoryName;}

	public Long getIdProduct() {return idProduct;}
	public void setIdProduct(Long idProduct) {this.idProduct = idProduct;}
	public String getProductName() {return productName;}
	public void setProductName(String productName) {this.productName = productName;}

	public Long getIdIngredient() {return idIngredient;}
	public void setIdIngredient(Long idIngredient) {this.idIngredient = idIngredient;}

	public String getIngredientName() {return ingredientName;}
	public void setIngredientName(String ingredientName) {this.ingredientName = ingredientName;}

	public Long getIdRecipe() {return idRecipe;}
	public void setIdRecipe(Long idRecipe) {this.idRecipe = idRecipe;}

	public Date getEvaluationDate() {return evaluationDate;}
	public void setEvaluationDate(Date evaluationDate) {this.evaluationDate = evaluationDate;}

	public Float getIngredientMeanPercentage() { return this.ingredientMeanPercentage;}
	public void setIngredientMeanPercentage(Float ingredientMeanPercentage) {this.ingredientMeanPercentage = ingredientMeanPercentage;}

	public Float getIngredientStdPercentage() { return this.ingredientStdPercentage;}
	public void setIngredientStdPercentage(Float ingredientStdPercentage) {this.ingredientStdPercentage = ingredientStdPercentage;}

	public List<ResultItemVO> getResultList() {return resultList;}
	public void setResultList(List<ResultItemVO> resultList) {this.resultList = resultList;}

}
