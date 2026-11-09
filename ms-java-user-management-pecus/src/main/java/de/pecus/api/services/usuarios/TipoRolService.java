package de.pecus.api.services.usuarios;

import java.util.List;

import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.roles.CreateTipoRolRequestVO;
import de.pecus.api.vo.roles.DeleteTipoRolRequestVO;
import de.pecus.api.vo.roles.FindDetailTipoRolRequestVO;
import de.pecus.api.vo.roles.FindDetailTipoRolResponseVO;
import de.pecus.api.vo.roles.FindListTipoRolRequestVO;
import de.pecus.api.vo.roles.FindListTipoRolResponseVO;
import de.pecus.api.vo.roles.UpdateTipoRolRequestVO;

/**
 * Clase de logica de negocio para administracion de TipoRoles
 * 
 * @author Proa
 *
 */
public interface TipoRolService {

	/**
	 * Crea un nuevo registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id generado
	 */
	ResponseVO<Long> create (RequestVO<CreateTipoRolRequestVO> request);

	/**
	 * Actualiza un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id actualizado
	 */
	ResponseVO<Long> update(RequestVO<UpdateTipoRolRequestVO> request);

	/**
	 * Marca un registro como eliminado un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id eliminado
	 */
	ResponseVO<Boolean> delete(RequestVO<DeleteTipoRolRequestVO> request);

	/**
	 * Consulta un registro
	 * 
	 * @param numero Nombre  buscado
	 * 
	 * @return Objeto VO con los datos encontrados
	 */
	ResponseVO<FindDetailTipoRolResponseVO> findDetail(RequestVO<FindDetailTipoRolRequestVO> request);

	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada 
	 */
	ResponseVO<List<FindListTipoRolResponseVO>> findList(RequestVO<FindListTipoRolRequestVO> request);



}
