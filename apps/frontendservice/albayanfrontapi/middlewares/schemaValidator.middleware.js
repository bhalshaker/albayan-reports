import Ajv from "ajv";
import addFormats from "ajv-formats";
const ajv = new Ajv({ allErrors: true });

addFormats(ajv);

const validateSchemas = (schema, source) => (request, reponse, next) => {
  // Allow shorthand "param" -> "params"
  if (source === "param") source = "params";

  // Validate the specified part of the request (body, params, query)
  let dataToValidate = request[source];

  // only process if source is body and body is a string (from form-data)
  if (
    source === "body" &&
    dataToValidate &&
    typeof dataToValidate.body === "string"
  ) {
    try {
      dataToValidate = JSON.parse(dataToValidate.body);
    } catch (err) {
      return reponse.status(400).json({
        success: false,
        message: "Validation error: invalid JSON in form field 'body'",
        details: [{ message: "Invalid JSON in 'body' form field" }],
        data: null,
      });
    }
  }

  // Handle case where params schema expects a single value
  if (
    source === "params" &&
    dataToValidate &&
    typeof dataToValidate === "object" &&
    !Array.isArray(dataToValidate)
  ) {
    const schemaType = schema && schema.type ? schema.type : null;
    const keys = Object.keys(dataToValidate || {});
    if (schemaType && schemaType !== "object" && keys.length === 1) {
      dataToValidate = dataToValidate[keys[0]];
    }
  }

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
