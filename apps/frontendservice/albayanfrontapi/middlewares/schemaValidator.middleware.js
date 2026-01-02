import Ajv from "ajv";
const ajv = new Ajv({ allErrors: true });

const validateSchemas = (schema, source) => (request, reponse, next) => {
  // Validate the specified part of the request (body, params, query)
  const dataToValidate = request[source];
  const validate = ajv.compile(schema);
  // Perform validation
  const isValid = validate(dataToValidate);
  // If validation fails, respond with 400 and error details
  if (!isValid) {
    return reponse.status(400).json({
      success: false,
      message: `Validation error: ${validate.errors}`,
      details: validate.errors,
      data: null,
    });
  }
  next();
};

export { validateSchemas };
