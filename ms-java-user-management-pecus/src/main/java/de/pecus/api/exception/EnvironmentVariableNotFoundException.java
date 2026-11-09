package de.pecus.api.exception;

import de.pecus.api.error.BusinessError;

public class EnvironmentVariableNotFoundException extends GeneralException {

    /**
     * Serial Version UID
     */
    private static final long serialVersionUID = 4487160263213435520L;

    public EnvironmentVariableNotFoundException(BusinessError businessError, Object... params) {
        super(businessError, params);
    }
}
