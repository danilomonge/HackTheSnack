package de.pecus.api.services.usuarios;

import java.util.List;

import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.brand.CreateBrandRequestVO;
import de.pecus.api.vo.brand.DeleteBrandRequestVO;
import de.pecus.api.vo.brand.FindDetailBrandRequestVO;
import de.pecus.api.vo.brand.FindDetailBrandResponseVO;
import de.pecus.api.vo.brand.FindListBrandRequestVO;
import de.pecus.api.vo.brand.FindListBrandResponseVO;
import de.pecus.api.vo.brand.UpdateBrandRequestVO;

/**
 * Clase de logica de negocio para administracion de Brandes
 * 
 * @author Proa
 *
 */
public interface BrandService {

	/**
	 * Crea un nuevo registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id generado
	 */
	ResponseVO<Long> create(RequestVO<CreateBrandRequestVO> request);

	/**
	 * Actualiza un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id actualizado
	 */
	ResponseVO<Long> update(RequestVO<UpdateBrandRequestVO> request);

	/**
	 * Marca un registro como eliminado un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id eliminado
	 */
	ResponseVO<Boolean> delete(RequestVO<DeleteBrandRequestVO> request);

	/**
	 * Consulta un registro
	 * 
	 * @param numero Nombre  buscado
	 * 
	 * @return Objeto VO con los datos encontrados
	 */
	ResponseVO<FindDetailBrandResponseVO> findDetail(RequestVO<FindDetailBrandRequestVO> request);

	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada 
	 */
	ResponseVO<List<FindListBrandResponseVO>> findList(RequestVO<FindListBrandRequestVO> request);



}
