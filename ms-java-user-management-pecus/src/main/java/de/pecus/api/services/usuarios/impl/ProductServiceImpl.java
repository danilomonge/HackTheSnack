package de.pecus.api.services.usuarios.impl;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;

import de.pecus.api.vo.product.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.stereotype.Service;

import de.pecus.api.constant.DataConstants;
import de.pecus.api.entities.BrandDO;
import de.pecus.api.entities.CategoryDO;
import de.pecus.api.entities.IngredientDO;
import de.pecus.api.entities.ProductDO;
import de.pecus.api.entities.RecipeDO;
import de.pecus.api.entities.SubCategoryDO;
import de.pecus.api.enums.WildcardTypeEnum;
import de.pecus.api.error.FuncionesBusinessError;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.repositories.usuarios.IngredientRepository;
import de.pecus.api.repositories.usuarios.ProductRepository;
import de.pecus.api.repositories.usuarios.RecipeRepository;
import de.pecus.api.services.usuarios.ProductService;
import de.pecus.api.util.CriteriaUtil;
import de.pecus.api.util.ResponseUtil;
import de.pecus.api.util.ServiceUtil;
import de.pecus.api.util.StringUtil;
import de.pecus.api.util.ValidatorArqUtil;
import de.pecus.api.util.ValidatorUtil;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;

/**
 * Clase de logica de negocio para administracion de productes
 * 
 * @author Proa
 *
 */
@Service
public class ProductServiceImpl implements ProductService {

	@Autowired
	private ProductRepository productRepository;

	@Autowired
	private IngredientRepository ingredientRepository;

	@Autowired
	private RecipeRepository recipeRepository;

	/**
	 * Crea un nuevo registro de product
	 * 
	 * @param request Objeto con parametros de entrada de product
	 * 
	 * @return Id generado
	 */
	public ResponseVO<Long> create(RequestVO<de.pecus.api.vo.product.CreateProductRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		
			// Validar los parametros de entrada
			if (validateParametersCreate(request, response)) {
		
				// Preparar los datos para actualizar la BB.DD.
				ProductDO productDO = new ProductDO();
				
				productDO.setName(request.getParameters().getName());
				productDO.setDescripcion(request.getParameters().getDescripcion());

				//Creamos las referencias a brand, category y subcategory
				BrandDO brandDO = new BrandDO();
				CategoryDO categoryDO = new CategoryDO();
				SubCategoryDO subCategoryDO = new SubCategoryDO();

				brandDO.setId(request.getParameters().getIdBrand());
				categoryDO.setId(request.getParameters().getIdCategory());
				subCategoryDO.setId(request.getParameters().getIdSubCategory());

				productDO.setBrand(brandDO);
				productDO.setCategory(categoryDO);
				productDO.setSubCategory(subCategoryDO);

				// Actualizar los parametros de auditoria
				ServiceUtil.setAuditFields(productDO, request.getToken());

				// Insertar el registro
				productDO = productRepository.saveAndFlush(productDO);

				// Regresar la respuesta correcta y el objeto a regresar
				response.setSuccess(true);
				response.setData(productDO.getId());
				
			}
		return response;
	}


	/**
	 * Actualiza un registro de product
	 * 
	 * @param request Objeto con parametros de entrada de product
	 * 
	 * @return Id actualizado
	 */
	public ResponseVO<Long> update(RequestVO<UpdateProductRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		ProductDO registroDO = new ProductDO();

		// Validar los campos de entrada
		if (validateParametersUpdate(request, response)) {
			
			UpdateProductRequestVO parameters = request.getParameters();

			registroDO.setId(parameters.getId());
			registroDO.setName(parameters.getName());
			registroDO.setDescripcion(parameters.getDescripcion());

			//Creamos las referencias a brand, category y subcategory
			BrandDO brandDO = new BrandDO();
			CategoryDO categoryDO = new CategoryDO();
			SubCategoryDO subCategoryDO = new SubCategoryDO();

			brandDO.setId(request.getParameters().getIdBrand());
			categoryDO.setId(request.getParameters().getIdCategory());
			subCategoryDO.setId(request.getParameters().getIdSubCategory());

			registroDO.setBrand(brandDO);
			registroDO.setCategory(categoryDO);
			registroDO.setSubCategory(subCategoryDO);

			// Actualizar parametros de auditoria
			ServiceUtil.setAuditFields(registroDO, request.getToken());

			// Actualizar el registro en BB.DD.
			registroDO = productRepository.saveAndFlush(registroDO);

			// Preparar respuesta y objeto actualizado
			response.setSuccess(true);
			response.setData(registroDO.getId());
		}
		return response;
	}


	/**
	 * Marca un registro como eliminado un registro de product
	 * 
	 * @param request Objeto con parametros de entrada de product
	 * 
	 * @return Id eliminado
	 */
	public ResponseVO<Boolean> delete(RequestVO<DeleteProductRequestVO> request) {

		// Declarar variables
		ResponseVO<Boolean> response = new ResponseVO<>();

		// Validar campos de entrada
		if (validateParametersDelete(request, response)) {

			ProductDO productDO = this.exists(request.getParameters().getId(), null);
			if (ValidatorUtil.isNull(productDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			}
			else {
			// Actualizar la informacion
			ServiceUtil.setDisabledEntity(productDO, request.getToken());
			
			// Actualizar la BB.DD.
			productDO = productRepository.saveAndFlush(productDO);

			// Preparar respuesta y objeto eliminado
			response.setSuccess(true);
			response.setData(Boolean.TRUE);
			}
		}
		return response;
	}

	/**
	 * Consulta un product por Identificador unico
	 * 
	 * @return Objeto VO con los datos encontrados
	 *
	 * @param request Objeto con los datos de busqueda
	 */
	public ResponseVO<FindDetailProductResponseVO> findDetail(RequestVO<FindDetailProductRequestVO> request) {

		// declaracion de varables
		ResponseVO<FindDetailProductResponseVO> response = new ResponseVO<>();
		FindDetailProductResponseVO salida = new FindDetailProductResponseVO();
		
		// validar que se cumplen las condiciones para realizar la consulta
		if (validateParametersFindDetail(request, response)) {

			ProductDO productDO = this.exists(request.getParameters().getId(), request.getParameters().getName());

			if (ValidatorUtil.isNull(productDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			} else {
				salida.setId(productDO.getId());
				salida.setName(productDO.getName());
				salida.setDescripcion(productDO.getDescripcion());
				salida.setIdBrand(productDO.getBrand().getId());
				salida.setNameBrand(productDO.getBrand().getName());
				salida.setIdCategory(productDO.getCategory().getId());
				salida.setNameCategory(productDO.getCategory().getName());
				salida.setIdSubCategory(productDO.getSubCategory().getId());
				salida.setNameSubCategory(productDO.getSubCategory().getName());

				response.setData(salida);
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
	public ResponseVO<List<FindListProductResponseVO>> findList(RequestVO<FindListProductRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListProductResponseVO>> response = new ResponseVO<>();
		
		Page<ProductDO> listaProduct = null;
		
		if (validateParametersFindByList(request, response)) {
	
			FindListProductRequestVO parameters = request.getParameters();
			// Se obtiene el idioma
			
			String  name 	= CriteriaUtil.validateNullLike(parameters.getName(), WildcardTypeEnum.BOTH_SIDES);
			
			// Preparamos el objeto para la paginacion
			String orderby = request.getOrderBy();
			String ordertype = request.getOrderType();
			String orderBy = ValidatorUtil.isNullOrEmpty(orderby) ? "id" : orderby;
			Direction orderType = ValidatorUtil.isNullOrEmpty(ordertype) || ordertype.equals("asc") ? Direction.ASC
					: Direction.DESC;
			Integer size = ValidatorUtil.isNullOrZero(request.getSize()) ? 10 : request.getSize();
			Integer page = ValidatorUtil.isNullOrZero(request.getPage()) ? 1 : request.getPage();
			Pageable pageable = PageRequest.of(page - 1, size, Sort.by(orderType, orderBy));
			
			String normalizedName = this.limpiarAcentos(parameters.getName());
			normalizedName = (this.cleanString(normalizedName));

			// ejecucion de la busqueda por el parametro recibido
			listaProduct = productRepository.findList(normalizedName, pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
 				if (ValidatorUtil.isNullOrEmpty(listaProduct.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaProduct.getTotalElements());
				response.setData(transformListDO(listaProduct.getContent()));
			}
		}
		return response;
	}

	/**
	 * Crea un nuevo registro de product
	 *
	 * @param request Objeto con parametros de entrada de product
	 *
	 * @return Id generado
	 */
	public ResponseVO<Long> associateProductIngredient(RequestVO<AssociateProductIngredientRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();

		// Validar los parametros de entrada
		if (validateParametersAssociate(request, response)) {

			// Preparar los datos para actualizar la BB.DD.
			RecipeDO recipeDO = new RecipeDO();
			IngredientDO ingredientDO = new IngredientDO();
			ProductDO productDO = new ProductDO();

			//Se considera un nuevo escenario que es la reactivacion de una relacion
			//Se buscara si existe previamente una relacion pero inactiva, y en tal caso se reactivara

			RecipeDO reciboBorradoDO = recipeRepository.findRecipeDelete(request.getParameters().getIdProduct(),
					request.getParameters().getIdIngredient());

			if (!ValidatorUtil.isNull(reciboBorradoDO)) {
				//Si el registro existe y estaba borrado se reactiva

				recipeDO = reciboBorradoDO;
				recipeDO.setActive(Boolean.TRUE);

			} else {

				//Se inserta el registro
				productDO.setId(request.getParameters().getIdProduct());
				ingredientDO.setId(request.getParameters().getIdIngredient());

				recipeDO.setProduct(productDO);
				recipeDO.setIngredient(ingredientDO);
				recipeDO.setFechaRegistro(request.getParameters().getFechaRegistro());

			}

			// Actualizar los parametros de auditoria
			ServiceUtil.setAuditFields(recipeDO, request.getToken());

			// Guardar los cambios
			recipeDO = recipeRepository.saveAndFlush(recipeDO);

			// Regresar la respuesta correcta y el objeto a regresar
			response.setSuccess(true);
			response.setData(recipeDO.getId());

		}
		return response;
	}

	/**
	 * Marca un registro como eliminado un registro de product
	 *
	 * @param request Objeto con parametros de entrada de product
	 *
	 * @return Id eliminado
	 */
	public ResponseVO<Boolean> deleteProductIngredient(RequestVO<DeleteProductIngredientRequestVO> request) {

		// Declarar variables
		ResponseVO<Boolean> response = new ResponseVO<>();

		// Validar campos de entrada
		if (validateParametersDeleteRecipe(request, response)) {

			RecipeDO recipeDO = this.existRecipe(request.getParameters().getIdRecipe(),
												 request.getParameters().getIdProduct(),
												 request.getParameters().getIdIngredient());

			if (ValidatorUtil.isNull(recipeDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			}
			else {
				// Actualizar la informacion
				ServiceUtil.setDisabledEntity(recipeDO, request.getToken());

				// Actualizar la BB.DD.
				recipeDO = recipeRepository.saveAndFlush(recipeDO);

				// Preparar respuesta y objeto eliminado
				response.setSuccess(true);
				response.setData(Boolean.TRUE);
			}
		}
		return response;
	}


	/**
	 * Consulta un Recipe por Id único o por producto e Ingrediente
	 *
	 * @return Objeto VO con los datos encontrados
	 *
	 * @param request Objeto con los datos de busqueda
	 */
	public ResponseVO<FindDetailRecipeResponseVO> findDetailRecipe(RequestVO<FindDetailRecipeRequestVO> request) {

		// declaracion de varables
		ResponseVO<FindDetailRecipeResponseVO> response = new ResponseVO<>();
		FindDetailRecipeResponseVO salida = new FindDetailRecipeResponseVO();

		// validar que se cumplen las condiciones para realizar la consulta
		if (validateParametersFindDetailRecipe(request, response)) {

			RecipeDO recipeDO = this.existRecipe(request.getParameters().getId(),
												request.getParameters().getIdProduct(),
												request.getParameters().getIdIngredient());

			if (ValidatorUtil.isNull(recipeDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			} else {

				salida.setId(recipeDO.getId());
				salida.setIdProduct(recipeDO.getProduct().getId());
				salida.setIdIngredient(recipeDO.getIngredient().getId());
				salida.setNameProduct(recipeDO.getProduct().getName());
				salida.setNameIngredient(recipeDO.getIngredient().getName());
				salida.setFechaRegistro(recipeDO.getFechaRegistro());

				response.setData(salida);
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
	public ResponseVO<List<FindListProductRecipeResponseVO>> findListRecipe(RequestVO<FindListProductRecipeRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListProductRecipeResponseVO>> response = new ResponseVO<>();

		Page<RecipeDO> listaRegisters = null;

		if (validateParametersFindByListRecipe(request, response)) {

			FindListProductRecipeRequestVO parameters = request.getParameters();

			// Preparamos el objeto para la paginacion
			String orderby = request.getOrderBy();
			String ordertype = request.getOrderType();
			String orderBy = ValidatorUtil.isNullOrEmpty(orderby) ? "id" : orderby;
			Direction orderType = ValidatorUtil.isNullOrEmpty(ordertype) || ordertype.equals("asc") ? Direction.ASC
					: Direction.DESC;
			Integer size = ValidatorUtil.isNullOrZero(request.getSize()) ? 10 : request.getSize();
			Integer page = ValidatorUtil.isNullOrZero(request.getPage()) ? 1 : request.getPage();
			Pageable pageable = PageRequest.of(page - 1, size, Sort.by(orderType, orderBy));

			// ejecucion de la busqueda por el parametro recibido
			listaRegisters = recipeRepository.findListByProduct(parameters.getIdProduct(), pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
			if (ValidatorUtil.isNullOrEmpty(listaRegisters.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaRegisters.getTotalElements());
				response.setData(transformListRecipeDO(listaRegisters.getContent()));
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
	 * Valida que los parametros para la operacion de insercion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersCreate(RequestVO<CreateProductRequestVO> request, ResponseVO<Long> response) {
		
		// Obtener los parametros de entrada
		CreateProductRequestVO parameters = request.getParameters();

		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getName())) {
			ResponseUtil.addError(request, response, 
					FuncionesBusinessError.REQUIRED_ID_NOMBRE_ERROR, request);
		} else {
			// Validacion de tamano
			String name = StringUtil.substring(parameters.getName(), DataConstants.MAX_SIZE_ID_NOMBRE);

			// Validacion de formato
			parameters.setName(StringUtil.toUpperCase(name));

				ProductDO registroB = this.exists(null,parameters.getName());
				
				if (!ValidatorUtil.isNull(registroB)) {
					ResponseUtil.addError(request, response, 
							FuncionesBusinessError.DUPLICATED_ERROR, request);					
			}
		}
		
		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getDescripcion())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_DESCRIPCION_ERROR,request);
		} else {
			// Validacion de tamano
			parameters.setDescripcion(StringUtil.substring(parameters.getDescripcion(), DataConstants.MAX_SIZE_DESCRIPCION));
		}
		
				
		// Regresar el resultado de la validacion
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de actualizacion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersUpdate(RequestVO<UpdateProductRequestVO> request, ResponseVO<Long> response) {
		// Recuperar parametros de entrada
		UpdateProductRequestVO parameters = request.getParameters();
		ProductDO registroUpdate = new ProductDO();
		
		// Validar que se informaron los campos de entrada
		if (ValidatorUtil.isNull(parameters)) {
			// Si no se ha informado regresar el error y no seguir validando
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}
		
		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getId()))
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR, request);
			return false;
		} else {
			
				registroUpdate = this.exists(parameters.getId(),null);
			
				if (ValidatorUtil.isNull(registroUpdate)) {
					ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
					return false;
				}
		}
		
		// Validaciones de campos obligatorios: NOMBRE
		if (!StringUtil.isNullOrEmpty(parameters.getName())) {
			// Validacion de tamano
			String name = StringUtil.substring(parameters.getName(), DataConstants.MAX_SIZE_ID_NOMBRE);

			// Validacion de formato
			parameters.setName(StringUtil.toUpperCase(name));
			
				//Validar la posible duplicidad del name
				ProductDO productBusqueda = this.exists(null, request.getParameters().getName());
				
				if (!ValidatorUtil.isNull(productBusqueda)) {
					//Si se encuentra el registro validamos que no sea el mismo Id
					if (registroUpdate.getId() != productBusqueda.getId()) {
						ResponseUtil.addError(request, response, FuncionesBusinessError.DUPLICATED_ERROR, request);
						
					}
			}
		} else {
			parameters.setName(registroUpdate.getName());
		}
		
		// Validaciones de campos obligatorios: DESCRIPCION
		if (!StringUtil.isNullOrEmpty(parameters.getDescripcion())) {
			// Validacion de tamano
			parameters.setDescripcion(
					StringUtil.substring(parameters.getDescripcion(), DataConstants.MAX_SIZE_DESCRIPCION));

		} else {
			parameters.setDescripcion(registroUpdate.getDescripcion());
		}
					
		// Retorna el resultado de la validacion.
		return ValidatorUtil.isSuccessfulResponse(response);
		
	}

	/**
	 * Valida que los parametros para la operacion de eliminacion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersDelete(RequestVO<DeleteProductRequestVO> request, ResponseVO<Boolean> response) {

		// Validar que se han informado los parametros de entrada
		if (ValidatorUtil.isNull(request.getParameters())) {
			// Si no se han informado generar error y terminar de validar
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}

		// Validaciones de campos obligatorios
		if (ValidatorUtil.isNullOrZero(request.getParameters().getId())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
		}
		
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
	private boolean validateParametersFindDetail(RequestVO<FindDetailProductRequestVO> request, ResponseVO<FindDetailProductResponseVO> response) {

		// Recuperar los parametros de entrada
		FindDetailProductRequestVO parameters = request.getParameters();

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(parameters.getId())) {
			
			//Buscar por criterio: Name
			if (ValidatorUtil.isNullOrEmpty(parameters.getName())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
			}
			else { 
				// Validacion de formato (Capital letters)
				parameters.setName(StringUtil.toUpperCase(parameters.getName()));
			}
		}
		
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
	private boolean validateParametersFindDetailRecipe(RequestVO<FindDetailRecipeRequestVO> request, ResponseVO<FindDetailRecipeResponseVO> response) {

		// Recuperar los parametros de entrada
		FindDetailRecipeRequestVO parameters = request.getParameters();

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(parameters.getId())) {

			//Buscar por criterio: product and ingredient
			if (ValidatorUtil.isNullOrZero(parameters.getIdProduct()) || ValidatorUtil.isNullOrZero(parameters.getIdIngredient()) ) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
			}
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
	private boolean validateParametersFindByList(RequestVO<FindListProductRequestVO> request,
			ResponseVO<List<FindListProductResponseVO>> response) {
		
		// Validar campos obligatorios
	    ValidatorArqUtil.validateParameters(request, response);
		
		// validar los parametros de la paginacion
	    ValidatorArqUtil.validatePaginatonParameters(request, response);
		return ValidatorUtil.isSuccessfulResponse(response);

	}



	/**
	 * Obtiene una lista de objetos productVO a partir de una lista de DO
	 * 
	 * @return Lista VO para retorno de resultados
	 * 
	 * @param listaProduct a transformar
	 */
	private List<FindListProductResponseVO> transformListDO(List<ProductDO> listaProduct) {

		// Declarar variables
		List<FindListProductResponseVO> listaProductVO = new ArrayList<>();

		// recorrer el objeto origen
		for (ProductDO productDO : listaProduct) {
			// Se hace la declaracion de variables necesarias
			FindListProductResponseVO productVO = new FindListProductResponseVO();
			
			productVO.setId(productDO.getId());
			productVO.setName(productDO.getName());
			productVO.setDescripcion(productDO.getDescripcion());
			productVO.setNameBrand(productDO.getBrand().getName());
			productVO.setIdCategory(productDO.getCategory().getId());
			productVO.setNameCategory(productDO.getCategory().getName());
			productVO.setIdSubCategory(productDO.getSubCategory().getId());
			productVO.setNameSubCategory(productDO.getSubCategory().getName());

			listaProductVO.add(productVO);
		}

		return listaProductVO;
	}

	/**
	 * Valida que los parametros para la operacion "asociar una substancia a producto
	 *
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersAssociate(RequestVO<AssociateProductIngredientRequestVO> request, ResponseVO<Long> response) {

		// Obtener los parametros de entrada
		AssociateProductIngredientRequestVO parameters = request.getParameters();

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(parameters.getIdProduct())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_PRODUCT_ERROR);
		} else {
			// validar que el campo obligatorio
			ProductDO productDO	= exists(parameters.getIdProduct(), null);
			if (ValidatorUtil.isNull(productDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_PRODUCT);
			}
		}

		if (ValidatorUtil.isNullOrZero(parameters.getIdIngredient())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_INGREDIENT_ERROR);
		} else {
			// validar que el campo obligatorio
			IngredientDO ingredientDO	= existIngredient(parameters.getIdIngredient());
			if (ValidatorUtil.isNull(ingredientDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_INGREDIENT);
			}
		}

		//Si no hay un error previo buscamos en la base de datos si no existe la relacion
		if (ValidatorUtil.isSuccessfulResponse(response)) {

			RecipeDO recipeDO = recipeRepository.findByProductAndIngredient(parameters.getIdProduct(),parameters.getIdIngredient());
			if (!ValidatorUtil.isNull(recipeDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.DUPLICATED_ERROR);
			}
		}

		// Regresar el resultado de la validacion
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de eliminacion sean correctos
	 *
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersDeleteRecipe(RequestVO<DeleteProductIngredientRequestVO> request, ResponseVO<Boolean> response) {

		// Validar que se han informado los parametros de entrada
		if (ValidatorUtil.isNull(request.getParameters())) {
			// Si no se han informado generar error y terminar de validar
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}

		// Validaciones de campos obligatorios
		if (ValidatorUtil.isNullOrZero(request.getParameters().getIdRecipe())) {
			if ((ValidatorUtil.isNullOrZero(request.getParameters().getIdProduct()))  || (ValidatorUtil.isNullOrZero(request.getParameters().getIdIngredient()))) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
			}
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
	private boolean validateParametersFindByListRecipe(RequestVO<FindListProductRecipeRequestVO> request,
												 ResponseVO<List<FindListProductRecipeResponseVO>> response) {

		// Validar campos obligatorios
		ValidatorArqUtil.validateParameters(request, response);

		// Validaciones de campos obligatorios
		if (ValidatorUtil.isNullOrZero(request.getParameters().getIdProduct())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
		}

		// validar los parametros de la paginacion
		ValidatorArqUtil.validatePaginatonParameters(request, response);
		return ValidatorUtil.isSuccessfulResponse(response);

	}

	/**
	 * Obtiene una lista de objetos productVO a partir de una lista de DO
	 *
	 * @return Lista VO para retorno de resultados
	 *
	 * @param listaRecipe a transformar
	 */
	private List<FindListProductRecipeResponseVO> transformListRecipeDO(List<RecipeDO> listaRecipe) {

		// Declarar variables
		List<FindListProductRecipeResponseVO> listaRecipeVO = new ArrayList<>();

		// recorrer el objeto origen
		for (RecipeDO recipeDO : listaRecipe) {
			// Se hace la declaracion de variables necesarias
			FindListProductRecipeResponseVO recipeVO = new FindListProductRecipeResponseVO();

			recipeVO.setId(recipeDO.getId());
			recipeVO.setIdProduct(recipeDO.getProduct().getId());
			recipeVO.setNameProduct(recipeDO.getProduct().getName());
			recipeVO.setIdIngredient(recipeDO.getIngredient().getId());
			recipeVO.setNameIngredient(recipeDO.getIngredient().getName());

			listaRecipeVO.add(recipeVO);
		}

		return listaRecipeVO;
	}


	/*************************************************************************
	 * Metodo que busca un registro por su id, name
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 * 
	 *************************************************************************/
	public ProductDO exists(Long id, String name){

		ProductDO registro = null;
		try {
			//Validacion de datos de entrada
			if (ValidatorUtil.isNullOrZero(id)) {
				if (ValidatorUtil.isNullOrEmpty(name)) {
					registro = null;
				} else {
					//Buscamos por nombre
					registro = productRepository.findByName(name);
				}
			} else {
				//Consulta
				registro = productRepository.findById(id);
			}
			//Validacion de existencia
			if (ValidatorUtil.isNull(registro)) {
				//Genera error
				registro = null;
			}
		} catch (Exception e) {
			registro = null;
		}
		
		return registro;
	}

	/*************************************************************************
	 * Metodo que busca un registro por su id
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 *
	 *************************************************************************/
	public IngredientDO existIngredient(Long idRegistro){

		IngredientDO registro = null;

		try {
			//Validacion de datos de entrada
			if (ValidatorUtil.isNullOrZero(idRegistro)) {
					registro = null;
				} else {
					registro = ingredientRepository.findById(idRegistro);
				}
			//Validacion de existencia
		} catch (Exception e) {
			registro = null;
		}

		return registro;
	}

	/*************************************************************************
	 * Metodo que busca un registro por su id
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 *
	 *************************************************************************/
	public RecipeDO existRecipe(Long idRecipe, Long idProduct, Long idIngredient){

		RecipeDO registro = null;

		try {
			//Validacion de datos de entrada
			if (ValidatorUtil.isNullOrZero(idRecipe)) {
				registro = recipeRepository.findByProductAndIngredient(idProduct,idIngredient);
			} else {
				registro =recipeRepository.findById(idRecipe);
			}
			//Validacion de existencia
		} catch (Exception e) {
			registro = null;
		}

		return registro;
	}



	public String cleanString(String strInput) {
		if(!ValidatorUtil.isNullOrEmpty(strInput)) {
			strInput = strInput.trim().toUpperCase();
		}
		return strInput; 
	}
	
	public String limpiarAcentos(String cadena) {
	    String limpio ="";
	    if (cadena !=null) {
	        String valor = cadena;
	        valor = valor.toUpperCase();
	        // Normalizar texto para eliminar acentos, dieresis, cedillas y tildes
	        limpio = Normalizer.normalize(valor, Normalizer.Form.NFD);
	        // Quitar caracteres no ASCII excepto la enie, interrogacion que abre, exclamacion que abre, grados, U con dieresis.
	        limpio = limpio.replaceAll("[^\\p{ASCII}(N\u0303)(n\u0303)(\u00A1)(\u00BF)(\u00B0)(U\u0308)(u\u0308)]", "");
	        // Regresar a la forma compuesta, para poder comparar la enie con la tabla de valores
	        limpio = Normalizer.normalize(limpio, Normalizer.Form.NFC);
	    }
	    return limpio;
	}
	
	
}
