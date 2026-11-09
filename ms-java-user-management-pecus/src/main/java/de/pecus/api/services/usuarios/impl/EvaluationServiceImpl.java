package de.pecus.api.services.usuarios.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.stereotype.Service;

import de.pecus.api.entities.BrandDO;
import de.pecus.api.entities.CategoryDO;
import de.pecus.api.entities.EvaluationDO;
import de.pecus.api.entities.IngredientDO;
import de.pecus.api.entities.ProductDO;
import de.pecus.api.entities.RecipeDO;
import de.pecus.api.entities.ResultItemDO;
import de.pecus.api.entities.SubCategoryDO;
import de.pecus.api.error.FuncionesBusinessError;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.repositories.usuarios.EvaluationRepository;
import de.pecus.api.repositories.usuarios.IngredientRepository;
import de.pecus.api.repositories.usuarios.ProductRepository;
import de.pecus.api.repositories.usuarios.RecipeRepository;
import de.pecus.api.repositories.usuarios.ResultItemRepository;
import de.pecus.api.services.usuarios.EvaluationService;
import de.pecus.api.util.ResponseUtil;
import de.pecus.api.util.ServiceUtil;
import de.pecus.api.util.ValidatorArqUtil;
import de.pecus.api.util.ValidatorUtil;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.evaluation.CreateEvaluationRequestVO;
import de.pecus.api.vo.evaluation.CreateResultItemVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationResponseVO;
import de.pecus.api.vo.evaluation.FindListEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindListEvaluationResponseVO;
import de.pecus.api.vo.evaluation.ResultItemVO;

/**
 * Clase de logica de negocio para administracion de evaluationes
 * 
 * @author Proa
 *
 */
@Service
public class EvaluationServiceImpl implements EvaluationService {

	@Autowired
	private EvaluationRepository evaluationRepository;

	@Autowired
	private ProductRepository productRepository;

	@Autowired
	private IngredientRepository ingredientRepository;

	@Autowired
	private RecipeRepository recipeRepository;

	@Autowired
	private ResultItemRepository resultItemRepository;

	/**
	 * Crea un nuevo registro de evaluation
	 * 
	 * @param request Objeto con parametros de entrada de evaluation
	 * 
	 * @return Id generado
	 */
	public ResponseVO<Long> create(RequestVO<CreateEvaluationRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		BrandDO	brandDO = new BrandDO();
		CategoryDO categoryDO = new CategoryDO();
		SubCategoryDO subCategoryDO = new SubCategoryDO();
		ProductDO productDO = new ProductDO();
		IngredientDO ingredientDO = new IngredientDO();
		RecipeDO recipeDO = new RecipeDO();

		
			// Validar los parametros de entrada
			if (validateParametersCreate(request, response)) {
		
				// Prepare data to insert in the database.
				EvaluationDO evaluationDO = new EvaluationDO();

				// create object foreing keys
				brandDO.setId(1L);
				categoryDO.setId(1L);
				subCategoryDO.setId(1L);
				productDO.setId(request.getParameters().getIdProduct());
				ingredientDO.setId(request.getParameters().getIdIngredient());
				recipeDO.setId(request.getParameters().getIdRecipe());

				// principal atributes
				evaluationDO.setBrand(brandDO);
				evaluationDO.setCategory(categoryDO);
				evaluationDO.setSubCategory(subCategoryDO);
				evaluationDO.setProduct(productDO);
				evaluationDO.setIngredient(ingredientDO);
				evaluationDO.setRecipe(recipeDO);
				evaluationDO.setEvaluationDate(request.getParameters().getEvaluationDate());
				evaluationDO.setIngredientMeanPercentage(request.getParameters().getIngredientMeanPercentage());
				evaluationDO.setIngredientStdPercentage(request.getParameters().getIngredientStdPercentage());

				// user information
				ServiceUtil.setAuditFields(evaluationDO, request.getToken());

				// insert into the database
				evaluationDO = evaluationRepository.saveAndFlush(evaluationDO);

				// Regresar la respuesta correcta y el objeto a regresar
				response.setSuccess(true);
				response.setData(evaluationDO.getId());

				if (!request.getParameters().getResultList().isEmpty()) {
					// insert resultlist into the database
					response.setSuccess(insertResultList(request, evaluationDO));
				}

			}
		return response;
	}


	/**
	 * Consulta un evaluation por Identificador unico
	 * 
	 * @return Objeto VO con los datos encontrados
	 *
	 * @param request Objeto con los datos de busqueda
	 */
	public ResponseVO<FindDetailEvaluationResponseVO> findDetail(RequestVO<FindDetailEvaluationRequestVO> request) {

		// declaracion de varables
		ResponseVO<FindDetailEvaluationResponseVO> response = new ResponseVO<>();
		FindDetailEvaluationResponseVO evaluationVO = new FindDetailEvaluationResponseVO();
		List<ResultItemVO> resultListVO = new ArrayList<>();

		// validar que se cumplen las condiciones para realizar la consulta
		if (validateParametersFindDetail(request, response)) {

			EvaluationDO evaluationDO = this.exists(request.getParameters().getId());

			if (ValidatorUtil.isNull(evaluationDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			} else {

				evaluationVO.setId(evaluationDO.getId());
				evaluationVO.setIdBrand(evaluationDO.getBrand().getId());
				evaluationVO.setBrandName(evaluationDO.getBrand().getName());
				evaluationVO.setIdCategory(evaluationDO.getCategory().getId());
				evaluationVO.setCategoryName(evaluationDO.getCategory().getName());
				evaluationVO.setIdSubCategory(evaluationDO.getSubCategory().getId());
				evaluationVO.setSubCategoryName(evaluationDO.getSubCategory().getName());
				evaluationVO.setIdProduct(evaluationDO.getProduct().getId());
				evaluationVO.setProductName(evaluationDO.getProduct().getName());
				evaluationVO.setIdIngredient(evaluationDO.getIngredient().getId());
				evaluationVO.setIngredientName(evaluationDO.getIngredient().getName());
				evaluationVO.setIdRecipe(evaluationDO.getRecipe().getId());
				evaluationVO.setIngredientMeanPercentage(evaluationDO.getIngredientMeanPercentage());
				evaluationVO.setIngredientStdPercentage(evaluationDO.getIngredientStdPercentage());
				evaluationVO.setEvaluationDate(evaluationDO.getEvaluationDate());

				//Recover items results for the evaluation
				resultListVO =recoverResultList(evaluationDO.getId());

				evaluationVO.setResultList(resultListVO);

				response.setData(evaluationVO);
				// regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
			}
				
		}
			
		return response;
	}



	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada de banner
	 */
	public ResponseVO<List<FindListEvaluationResponseVO>> findList(RequestVO<FindListEvaluationRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListEvaluationResponseVO>> response = new ResponseVO<>();
		
		Page<EvaluationDO> listaEvaluation = null;
		
		if (validateParametersFindByList(request, response)) {
	
			FindListEvaluationRequestVO parameters = request.getParameters();

			// Preparamos el objeto para la paginacion
			String orderby = request.getOrderBy();
			String ordertype = request.getOrderType();
			String orderBy = ValidatorUtil.isNullOrEmpty(orderby) ? "id" : orderby;
			Direction orderType = ValidatorUtil.isNullOrEmpty(ordertype) || ordertype.equals("asc") ? Direction.ASC
					: Direction.DESC;
			Integer size = ValidatorUtil.isNullOrZero(request.getSize()) ? 10 : request.getSize();
			Integer page = ValidatorUtil.isNullOrZero(request.getPage()) ? 1 : request.getPage();
			Pageable pageable = PageRequest.of(page - 1, size, Sort.by(orderType, orderBy));

			// Database execution
			listaEvaluation = evaluationRepository.findList(request.getParameters().getIdProduct(), pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
 				if (ValidatorUtil.isNullOrEmpty(listaEvaluation.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaEvaluation.getTotalElements());
				response.setData(transformListDO(listaEvaluation.getContent()));
			}
		}
		return response;
	}


	/**
	 * Consulta la base de datos de resultados para un producto y/o ingrediente
	 *
	 * @return ReponseVO con los datos encontrados
	 *
	 * @param request Objeto con parametros de entrada de banner
	 */
	public ResponseVO<List<FindListEvaluationResponseVO>> findListProductIngredientResult(RequestVO<FindListEvaluationRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListEvaluationResponseVO>> response = new ResponseVO<>();

		Page<ResultItemDO> listaResultado = null;

		if (validateParametersFindByListProductIngredientResult(request, response)) {

			FindListEvaluationRequestVO parameters = request.getParameters();

			// Preparamos el objeto para la paginacion
			Pageable pageable = null;
			String orderby = request.getOrderBy();
			String ordertype = request.getOrderType();
			String orderBy = ValidatorUtil.isNullOrEmpty(orderby) ? "id" : orderby;
			Direction orderType = ValidatorUtil.isNullOrEmpty(ordertype) || ordertype.equals("asc") ? Direction.ASC
					: Direction.DESC;

			Integer size = ValidatorUtil.isNullOrZero(request.getSize()) ? 100 : request.getSize();
			Integer page = ValidatorUtil.isNullOrZero(request.getPage()) ? 1 : request.getPage();

			// OrderBy criteria
            if (!ValidatorUtil.isNull(parameters.getIdProduct())) {
				//Information for one product:  list of results order by ingredients and date
				 pageable = PageRequest.of(page - 1, size, Sort.by(orderType, "i.id","evaluationDate"));
            } else {
                if (!ValidatorUtil.isNull(parameters.getIdIngredient())) {
					//Information for one ingredient:  list of results order by product and date
					 pageable = PageRequest.of(page - 1, size, Sort.by(orderType, "p.id", "evaluationDate"));
				} else {
					pageable = PageRequest.of(page - 1, size, Sort.by(orderType, orderBy));
				}
            }

            // Database execution
			listaResultado = resultItemRepository.findListProductIngredientResult(request.getParameters().getIdProduct(),
					request.getParameters().getIdIngredient(), pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
			if (ValidatorUtil.isNullOrEmpty(listaResultado.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaResultado.getTotalElements());
				response.setData(transformListResultItemDO(listaResultado.getContent()));
			}
		}
		return response;
	}


	/*******************************************************************************************************
	 * 
	 * FIN METODOS PUBLICOS
	 * 
	 *******************************************************************************************************/

	/*******************************************************************************************************
	 * 
	 * METODOS VALIDACION
	 * 
	 *******************************************************************************************************/

	/**
	 * This method validate all the entry data before create the object in the database
	 * 
	 * @param request  Data entry
	 * @param response response
	 * @return true if everything it´s ok
	 */
	private boolean validateParametersCreate(RequestVO<CreateEvaluationRequestVO> request, ResponseVO<Long> response) {
		
		// Obtener los parametros de entrada
		CreateEvaluationRequestVO parameters = request.getParameters();
		ProductDO productRegister = new ProductDO();
		IngredientDO ingredientRegister = new IngredientDO();
		RecipeDO recipeRegister = new RecipeDO();

		// Validar que se informaron los campos de entrada
		if (ValidatorUtil.isNull(parameters)) {
			// Si no se ha informado regresar el error y no seguir validando
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}

		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getIdProduct()))
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_PRODUCT_ERROR, request);
			return false;
		} else {

			productRegister = productRepository.findById(parameters.getIdProduct());

			if (ValidatorUtil.isNull(productRegister)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_PRODUCT, request);
				return false;
			}
		}

		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getIdIngredient()))
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_INGREDIENT_ERROR, request);
			return false;

		} else {

			ingredientRegister = ingredientRepository.findById(parameters.getIdIngredient());

			if (ValidatorUtil.isNull(ingredientRegister)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_INGREDIENT, request);
				return false;
			}
		}

		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getIdRecipe()))
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_RECIPE_ID_ERROR, request);
			return false;
		} else {

			recipeRegister = recipeRepository.findById(parameters.getIdRecipe());

			if (ValidatorUtil.isNull(recipeRegister)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_RECIPE_ID_ERROR, request);
				return false;
			} else {
				if (recipeRegister.getProduct().getId() != parameters.getIdProduct()) {
					ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_RECIPE_PRODUCT_ERROR, request);
					return false;

				} else {
					if (recipeRegister.getIngredient().getId() != parameters.getIdIngredient()) {
						ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_RECIPE_INGREDIENT_ERROR, request);
						return false;
					}
				}
			}
		}

		//Validar que exista el registro a actualizar
		if(parameters.getIngredientMeanPercentage() == 0)
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_INGREDIENT_MEAN_PERCENTAGE_ERROR, request);
			return false;
		}

		//Validar que exista el registro a actualizar
		if(parameters.getIngredientStdPercentage() == 0 )
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_INGREDIENT_STD_PERCENTAGE_ERROR, request);
			return false;
		}

		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getEvaluationDate()))
		{
            Date actualDate = new Date();
            parameters.setEvaluationDate(actualDate);

		}

		// Regresar el resultado de la validacion
		return ValidatorUtil.isSuccessfulResponse(response);
	}



	/**
	 * Valida que los parametros para la operacion de consulta por nombre sean
	 * correctos
	 * 
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los parametros a valida
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindDetail(RequestVO<FindDetailEvaluationRequestVO> request, ResponseVO<FindDetailEvaluationResponseVO> response) {

		// Recuperar los parametros de entrada
		FindDetailEvaluationRequestVO parameters = request.getParameters();

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(parameters.getId())) {
			
				ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
		}
		
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de consulta por parametros sean
	 * correctos
	 * 
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los criterios a buscar
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindByList(RequestVO<FindListEvaluationRequestVO> request,
			ResponseVO<List<FindListEvaluationResponseVO>> response) {
		
		// Validar campos obligatorios
	    ValidatorArqUtil.validateParameters(request, response);

		// validar los parametros de la paginacion
		ValidatorArqUtil.validatePaginatonParameters(request, response);

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(request.getParameters().getIdProduct())) {

			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
		}

		return ValidatorUtil.isSuccessfulResponse(response);

	}


	/**
	 * Valida que los parametros para la operacion de consulta por parametros sean
	 * correctos
	 *
	 * @return true si el nombre no esta vacio
	 *
	 * @param request  Objeto con los criterios a buscar
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindByListProductIngredientResult(RequestVO<FindListEvaluationRequestVO> request,
												 ResponseVO<List<FindListEvaluationResponseVO>> response) {

		// Validar campos obligatorios
		ValidatorArqUtil.validateParameters(request, response);

		// validar los parametros de la paginacion
		ValidatorArqUtil.validatePaginatonParameters(request, response);

		return ValidatorUtil.isSuccessfulResponse(response);

	}


	/**
	 * Obtiene una lista de objetos evaluationVO a partir de una lista de DO
	 * 
	 * @return Lista VO para retorno de resultados
	 * 
	 * @param listaEvaluation a transformar
	 */
	private List<FindListEvaluationResponseVO> transformListDO(List<EvaluationDO> listaEvaluation) {

		// Declarar variables
		List<FindListEvaluationResponseVO> listaEvaluationVO = new ArrayList<>();

		// recorrer el objeto origen
		for (EvaluationDO evaluationDO : listaEvaluation) {
			// Se hace la declaracion de variables necesarias
			FindListEvaluationResponseVO evaluationVO = new FindListEvaluationResponseVO();
			
			evaluationVO.setId(evaluationDO.getId());
			evaluationVO.setIdBrand(evaluationDO.getBrand().getId());
			evaluationVO.setBrandName(evaluationDO.getBrand().getName());
			evaluationVO.setIdCategory(evaluationDO.getCategory().getId());
			evaluationVO.setCategoryName(evaluationDO.getCategory().getName());
			evaluationVO.setIdSubCategory(evaluationDO.getSubCategory().getId());
			evaluationVO.setSubCategoryName(evaluationDO.getSubCategory().getName());
			evaluationVO.setIdProduct(evaluationDO.getProduct().getId());
			evaluationVO.setProductName(evaluationDO.getProduct().getName());
			evaluationVO.setIdIngredient(evaluationDO.getIngredient().getId());
			evaluationVO.setIngredientName(evaluationDO.getIngredient().getName());
			evaluationVO.setIdRecipe(evaluationDO.getRecipe().getId());
			evaluationVO.setEvaluationDate(evaluationDO.getEvaluationDate());
			evaluationVO.setIngredientMeanPercentage(evaluationDO.getIngredientMeanPercentage());
			evaluationVO.setIngredientStdPercentage(evaluationDO.getIngredientStdPercentage());

			listaEvaluationVO.add(evaluationVO);
		}

		return listaEvaluationVO;
	}


	/**
	 * Recover the list of results for a evaluation
	 *
	 * @return result list
	 *
	 * @param evaluation to recover results
	 */
	private List<ResultItemVO> recoverResultList(Long evaluation) {

		// Declarar variables
		List<ResultItemVO> resultListVO = new ArrayList<>();
		List<ResultItemDO> resultListDO = null;

		resultListDO = resultItemRepository.findAllResult(evaluation);

		if (!ValidatorUtil.isNull(resultListDO)) {
			// Loop for each result from data base
			for (ResultItemDO resultDO : resultListDO) {

				// new output object
				ResultItemVO resultItemVO = new ResultItemVO();

				//move data from database object to output object
				resultItemVO.setId(resultDO.getId());
				resultItemVO.setRecipeId(resultDO.getRecipe().getId());
				resultItemVO.setEvaluationId(resultDO.getEvaluation().getId());
				resultItemVO.setEvaluationDate(resultDO.getEvaluationDate());
				resultItemVO.setProductId(resultDO.getProduct().getId());
				resultItemVO.setIngredientId(resultDO.getIngredient().getId());
				resultItemVO.setIngredientName(resultDO.getIngredient().getName());
				resultItemVO.setIngredientMeanPercentage(resultDO.getIngredientMeanPercentage());
				resultItemVO.setIngredientStdPercentage(resultDO.getIngredientStdPercentage());

				//add object to the list
				resultListVO.add(resultItemVO);
			}
		}

		return resultListVO;
	}


	/**
	 * Obtiene una lista de objetos evaluationVO a partir de una lista de DO
	 *
	 * @return Lista VO para retorno de resultados
	 *
	 * @param listaResultado a transformar
	 */
	private List<FindListEvaluationResponseVO> transformListResultItemDO(List<ResultItemDO> listaResultado) {

		// Declarar variables
		List<FindListEvaluationResponseVO> listaEvaluationVO = new ArrayList<>();


		// recorrer el objeto origen
		for (ResultItemDO resultItemDO : listaResultado) {
			// Se hace la declaracion de variables necesarias
			FindListEvaluationResponseVO evaluationVO = new FindListEvaluationResponseVO();

			evaluationVO.setId(resultItemDO.getEvaluation().getId());
			evaluationVO.setIdBrand(resultItemDO.getProduct().getBrand().getId());
//			evaluationVO.setBrandName(resultItemDO.getProduct().getBrand().getName());
			evaluationVO.setIdCategory(resultItemDO.getProduct().getCategory().getId());
//			evaluationVO.setCategoryName(resultItemDO.getProduct().getCategory().getName());
			evaluationVO.setIdSubCategory(resultItemDO.getProduct().getSubCategory().getId());
//			evaluationVO.setSubCategoryName(resultItemDO.getProduct().getSubCategory().getName());
			evaluationVO.setIdProduct(resultItemDO.getProduct().getId());
			evaluationVO.setProductName(resultItemDO.getProduct().getName());
			evaluationVO.setIdIngredient(resultItemDO.getIngredient().getId());
			evaluationVO.setIngredientName(resultItemDO.getIngredient().getName());
			evaluationVO.setIdRecipe(resultItemDO.getRecipe().getId());
//          evaluationVO.setEvaluationDate(resultItemDO.getEvaluationDate());
			evaluationVO.setEvaluationDate(resultItemDO.getCreationDate());
			evaluationVO.setIngredientMeanPercentage(resultItemDO.getIngredientMeanPercentage());
			evaluationVO.setIngredientStdPercentage(resultItemDO.getIngredientStdPercentage());

			listaEvaluationVO.add(evaluationVO);
		}

		return listaEvaluationVO;
	}

	/**
	 * Insert into the database the differents result-items
	 *
	 * @return result list
	 *
	 */
	private Boolean insertResultList(RequestVO<CreateEvaluationRequestVO> request, EvaluationDO evaluationDO ) {

		// Declarar variables
		List<CreateResultItemVO> resultListVO = new ArrayList<>();
		List<ResultItemDO> resultListDO = new ArrayList<>();
		Boolean resultado = true;

		if (!ValidatorUtil.isNull(request.getParameters().getResultList())) {
			resultListVO = request.getParameters().getResultList();

			// Loop for each result from data base
			for (CreateResultItemVO resultVO : resultListVO) {

				// new output object
				ResultItemDO resultItemDO = new ResultItemDO();
				EvaluationDO evaluation = new EvaluationDO();
				ProductDO product = new ProductDO();
				IngredientDO ingredient = new IngredientDO();
				RecipeDO recipe = new RecipeDO();

				//move data from database object to output object
				evaluation.setId(evaluationDO.getId());
				product.setId(evaluationDO.getProduct().getId());

				ingredient.setId(resultVO.getIngredientId());
				recipe.setId(resultVO.getRecipeId());

				resultItemDO.setEvaluation(evaluation);
				resultItemDO.setProduct(product);
				resultItemDO.setIngredient(ingredient);
				resultItemDO.setRecipe(recipe);
				resultItemDO.setEvaluationDate(evaluationDO.getEvaluationDate());
				resultItemDO.setIngredientMeanPercentage(resultVO.getIngredientMeanPercentage());
				resultItemDO.setIngredientStdPercentage(resultVO.getIngredientStdPercentage());

				// user information
				ServiceUtil.setAuditFields(resultItemDO, request.getToken());


				//add object to the list
				resultListDO.add(resultItemDO);
			}

			if (!ValidatorUtil.isNull(resultListDO)) {
				resultListDO = resultItemRepository.saveAllAndFlush(resultListDO);
			} else {
				resultado = false;
			}
		}

		return resultado;
	}

	/*************************************************************************
	 * Metodo que busca un registro por su id, name
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 * 
	 *************************************************************************/
	public EvaluationDO exists(Long id){

		EvaluationDO registro = null;

		try {

			//Validacion de datos de entrada
			if (!ValidatorUtil.isNullOrZero(id)) {

				registro = evaluationRepository.findById(id);

			}

		} catch (Exception e) {
			registro = null;
		}
		
		return registro;
	}	


}
