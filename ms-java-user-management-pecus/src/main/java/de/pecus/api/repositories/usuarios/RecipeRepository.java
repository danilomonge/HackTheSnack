package de.pecus.api.repositories.usuarios;

import java.io.Serializable;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import de.pecus.api.entities.RecipeDO;

public interface RecipeRepository extends JpaRepository<RecipeDO, Serializable> {

	/**
	 * Consulta por id sin implementacion de query especifico
	 *
	 * @return Objeto de mapeo a la entidad
	 *
	 * @param id Identificador de registro buscado
	 */
	@Query(value = " SELECT r"
			+ " FROM  RecipeDO r"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient s"
			+ " WHERE r.active = true "
			+ " AND r.id = :id")
	RecipeDO findById(@Param("id") Long id);

	/**
	 * Consulta por producto y sustacia
	 * @return Objeto de mapeo a la entidad
	 */
	@Query(value = " SELECT r"
			+ " FROM  RecipeDO r"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient s"
			+ " WHERE r.active = true "
			+ " AND r.product.id = :idProduct"
			+ " AND r.ingredient.id = :idIngredient")
	RecipeDO findByProductAndIngredient(@Param("idProduct") Long idProduct, @Param("idIngredient") Long idIngredient);

	/**
	 * Consulta un registro por idProducto y idIngrediente
	 * con la caracteristica active=false, es decir que se habia borrado anteriormente
	 *
	 * @return Objeto de mapeo a la entidad
	 */
	@Query(value = " SELECT r"
			+ " FROM  RecipeDO r"
			+ " WHERE r.active = false "
			+ " AND r.product.id = :idProduct"
			+ " AND r.ingredient.id = :idIngredient")
	RecipeDO findRecipeDelete(@Param("idProduct") Long idProduct,@Param("idIngredient") Long idIngredient );



	/**
	 * Consulta la lista de ingredientes de un producto
	 *
	 * @return Objeto de mapeo a la entidad
	 */
	@Query(value = " SELECT r"
			+ " FROM  RecipeDO r"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient s"
			+ " WHERE r.active = true "
			+ " AND p.id = :idProduct",
			countQuery="SELECT COUNT(r) "
					+ " FROM  RecipeDO r"
					+ " INNER JOIN r.product p"
					+ " INNER JOIN r.ingredient s"
					+ " WHERE r.active = true "
				+ "	AND p.id = :idProduct")
	Page<RecipeDO> findListByProduct(@Param("idProduct") Long idProduct,
							 Pageable pageable);

	/**
	 * Consulta la lista de productos que tienen un ingrediente
	 *
	 * @return Objeto de mapeo a la entidad
	 */
	@Query(value = " SELECT r"
			+ " FROM  RecipeDO r"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient s"
			+ " WHERE r.active = true "
			+ " AND s.id = :idIngredient",
			countQuery="SELECT COUNT(r) "
					+ " FROM  RecipeDO r"
					+ " INNER JOIN r.product p"
					+ " INNER JOIN r.ingredient s"
					+ " WHERE r.active = true "
					+ "	AND s.id = :idIngredient")
	Page<RecipeDO> findListByIngredient(@Param("idIngredient") Long idIngredient,
									  Pageable pageable);


}
