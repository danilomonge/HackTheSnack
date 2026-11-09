package de.pecus.api.services.usuarios.impl;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang.math.RandomUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.stereotype.Service;

import de.pecus.api.constant.DataConstants;
import de.pecus.api.entities.IngredientDO;
import de.pecus.api.enums.WildcardTypeEnum;
import de.pecus.api.error.FuncionesBusinessError;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.repositories.usuarios.IngredientRepository;
import de.pecus.api.services.usuarios.IngredientService;
import de.pecus.api.util.CriteriaUtil;
import de.pecus.api.util.ResponseUtil;
import de.pecus.api.util.ServiceUtil;
import de.pecus.api.util.StringUtil;
import de.pecus.api.util.ValidatorArqUtil;
import de.pecus.api.util.ValidatorUtil;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.ingredient.CreateIngredientRequestVO;
import de.pecus.api.vo.ingredient.DeleteIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindDetailIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindDetailIngredientResponseVO;
import de.pecus.api.vo.ingredient.FindListIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindListIngredientResponseVO;
import de.pecus.api.vo.ingredient.UpdateIngredientRequestVO;

/**
 * Clase de logica de negocio para administracion de ingredientes
 * 
 * @author Proa
 *
 */
@Service
public class IngredientServiceImpl implements IngredientService {

	@Autowired
	private IngredientRepository ingredientRepository;


	/**
	 * Crea un nuevo registro de ingredient
	 * 
	 * @param request Objeto con parametros de entrada de ingredient
	 * 
	 * @return Id generado
	 */
	public ResponseVO<Long> create(RequestVO<CreateIngredientRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		
			// Validar los parametros de entrada
			if (validateParametersCreate(request, response)) { 
		
				// Preparar los datos para actualizar la BB.DD.
				IngredientDO ingredientDO = new IngredientDO();
				
				ingredientDO.setId(RandomUtils.nextLong());
				ingredientDO.setName(request.getParameters().getName());
				ingredientDO.setDescription(request.getParameters().getDescription());
				
				// Actualizar los parametros de auditoria
				ServiceUtil.setAuditFields(ingredientDO, request.getToken());

				// Insertar el registro
				ingredientDO = ingredientRepository.saveAndFlush(ingredientDO);

				// Regresar la respuesta correcta y el objeto a regresar
				response.setSuccess(true);
				response.setData(ingredientDO.getId());
				
			}
		return response;
	}


	/**
	 * Actualiza un registro de ingredient
	 * 
	 * @param request Objeto con parametros de entrada de ingredient
	 * 
	 * @return Id actualizado
	 */
	public ResponseVO<Long> update(RequestVO<UpdateIngredientRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		IngredientDO registroDO = new IngredientDO();

		// Validar los campos de entrada
		if (validateParametersUpdate(request, response)) {
			
			UpdateIngredientRequestVO parameters = request.getParameters();

			registroDO.setId(parameters.getId());
			registroDO.setName(parameters.getName());
			registroDO.setDescription(parameters.getDescription());
			
			// Actualizar parametros de auditoria
			ServiceUtil.setAuditFields(registroDO, request.getToken());

			// Actualizar el registro en BB.DD.
			registroDO = ingredientRepository.saveAndFlush(registroDO);

			// Preparar respuesta y objeto actualizado
			response.setSuccess(true);
			response.setData(registroDO.getId());
		}
		return response;
	}


	/**
	 * Marca un registro como eliminado un registro de ingredient
	 * 
	 * @param request Objeto con parametros de entrada de ingredient
	 * 
	 * @return Id eliminado
	 */
	public ResponseVO<Boolean> delete(RequestVO<DeleteIngredientRequestVO> request) {

		// Declarar variables
		ResponseVO<Boolean> response = new ResponseVO<>();

		// Validar campos de entrada
		if (validateParametersDelete(request, response)) {

			IngredientDO ingredientDO = this.exists(request.getParameters().getId(), null);
			if (ValidatorUtil.isNull(ingredientDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			}
			else {
			// Actualizar la informacion
			ServiceUtil.setDisabledEntity(ingredientDO, request.getToken());
			
			// Actualizar la BB.DD.
			ingredientDO = ingredientRepository.saveAndFlush(ingredientDO);

			// Preparar respuesta y objeto eliminado
			response.setSuccess(true);
			response.setData(Boolean.TRUE);
			}
		}
		return response;
	}

	/**
	 * Consulta un ingredient por Identificador unico
	 * 
	 * @return Objeto VO con los datos encontrados
	 * @param Id      Identificador del registro a buscar
	 * 
	 * @param request Objeto con los datos de busqueda
	 */
	public ResponseVO<FindDetailIngredientResponseVO> findDetail(RequestVO<FindDetailIngredientRequestVO> request) {

		// declaracion de varables
		ResponseVO<FindDetailIngredientResponseVO> response = new ResponseVO<>();
		FindDetailIngredientResponseVO salida = new FindDetailIngredientResponseVO();
		
		// validar que se cumplen las condiciones para realizar la consulta
		if (validateParametersFindDetail(request, response)) {

			IngredientDO ingredientDO = this.exists(request.getParameters().getId(), request.getParameters().getName());

			if (ValidatorUtil.isNull(ingredientDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			} else {
				salida.setId(ingredientDO.getId());
				salida.setName(ingredientDO.getName());
				salida.setDescription(ingredientDO.getDescription());

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
	public ResponseVO<List<FindListIngredientResponseVO>> findList(RequestVO<FindListIngredientRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListIngredientResponseVO>> response = new ResponseVO<>();
		
		Page<IngredientDO> listaIngredient = null;
		
		if (validateParametersFindByList(request, response)) {
	
			FindListIngredientRequestVO parameters = request.getParameters();
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
			
			String normalizedName = this.cleanString(this.limpiarAcentos(request.getParameters().getName()));
			normalizedName = (StringUtil.toUpperCase(normalizedName));

			// ejecucion de la busqueda por el parametro recibido
			listaIngredient = ingredientRepository.findList(normalizedName, pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
 				if (ValidatorUtil.isNullOrEmpty(listaIngredient.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaIngredient.getTotalElements());
				response.setData(transformListDO(listaIngredient.getContent()));
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
	private boolean validateParametersCreate(RequestVO<CreateIngredientRequestVO> request, ResponseVO<Long> response) {
		
		// Obtener los parametros de entrada
		CreateIngredientRequestVO parameters = request.getParameters();

		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getName())) {
			ResponseUtil.addError(request, response, 
					FuncionesBusinessError.REQUIRED_ID_NOMBRE_ERROR, request);
		} else {
			// Validacion de tamano
			String name = StringUtil.substring(parameters.getName(), DataConstants.MAX_SIZE_ID_NOMBRE);

			// Validacion de formato
			parameters.setName(StringUtil.toUpperCase(name));

				IngredientDO registroB = this.exists(null,parameters.getName());
				
				if (!ValidatorUtil.isNull(registroB)) {
					ResponseUtil.addError(request, response, 
							FuncionesBusinessError.DUPLICATED_ERROR, request);					
			}
		}
		
		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getDescription())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_DESCRIPCION_ERROR,request);
		} else {
			// Validacion de tamano
			parameters.setDescription(StringUtil.substring(parameters.getDescription(), DataConstants.MAX_SIZE_ID_NOMBRE));
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
	private boolean validateParametersUpdate(RequestVO<UpdateIngredientRequestVO> request, ResponseVO<Long> response) {
		// Recuperar parametros de entrada
		UpdateIngredientRequestVO parameters = request.getParameters();
		IngredientDO registroUpdate = new IngredientDO();
		
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
				IngredientDO ingredientBusqueda = this.exists(null, request.getParameters().getName());
				
				if (!ValidatorUtil.isNull(ingredientBusqueda)) {
					//Si se encuentra el registro validamos que no sea el mismo Id
					if (registroUpdate.getId() != ingredientBusqueda.getId()) {
						ResponseUtil.addError(request, response, FuncionesBusinessError.DUPLICATED_ERROR, request);
						
					}
			}
		} else {
			parameters.setName(registroUpdate.getName());
		}
		
		// Validaciones de campos obligatorios: Description
		if (!StringUtil.isNullOrEmpty(parameters.getDescription())) {
			// Validacion de tamano
			parameters.setDescription(
					StringUtil.substring(parameters.getDescription(), DataConstants.MAX_SIZE_ID_NOMBRE));

		} else {
			parameters.setDescription(registroUpdate.getDescription());
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
	private boolean validateParametersDelete(RequestVO<DeleteIngredientRequestVO> request, ResponseVO<Boolean> response) {

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
	 * @param Id Identificador del registro a buscar
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los parametros a valida
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindDetail(RequestVO<FindDetailIngredientRequestVO> request, ResponseVO<FindDetailIngredientResponseVO> response) {

		// Recuperar los parametros de entrada
		FindDetailIngredientRequestVO parameters = request.getParameters();

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
	 * Valida que los parametros para la operacion de consulta por parametros sean
	 * correctos
	 * 
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los criterios a buscar
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindByList(RequestVO<FindListIngredientRequestVO> request,
			ResponseVO<List<FindListIngredientResponseVO>> response) {
		
		// Validar campos obligatorios
	    ValidatorArqUtil.validateParameters(request, response);
		
		// validar los parametros de la paginacion
	    ValidatorArqUtil.validatePaginatonParameters(request, response);
		return ValidatorUtil.isSuccessfulResponse(response);

	}



	/**
	 * Obtiene una lista de objetos ingredientVO a partir de una lista de DO
	 * 
	 * @return Lista VO para retorno de resultados
	 * 
	 * @param listaIngredient a transformar
	 */
	private List<FindListIngredientResponseVO> transformListDO(List<IngredientDO> listaIngredient) {

		// Declarar variables
		List<FindListIngredientResponseVO> listaIngredientVO = new ArrayList<>();

		// recorrer el objeto origen
		for (IngredientDO ingredientDO : listaIngredient) {
			// Se hace la declaracion de variables necesarias
			FindListIngredientResponseVO ingredientVO = new FindListIngredientResponseVO();
			
			ingredientVO.setId(ingredientDO.getId());
			ingredientVO.setName(ingredientDO.getName());
			ingredientVO.setDescription(ingredientDO.getDescription());
			
			listaIngredientVO.add(ingredientVO);
		}

		return listaIngredientVO;
	}
	


	/*************************************************************************
	 * Metodo que busca un registro por su id, name
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 * 
	 *************************************************************************/
	public IngredientDO exists(Long id, String name){

		IngredientDO registro = null;
		try {
			//Validacion de datos de entrada
			if (ValidatorUtil.isNullOrZero(id)) {
				if (ValidatorUtil.isNullOrEmpty(name)) {
					registro = null;
				} else {
					//Buscamos por nombre
					registro = ingredientRepository.findByName(name);
				}
			} else {
				//Consulta
				registro = ingredientRepository.findById(id);
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
