import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class HttpMethodsPostTest {

    @Test
    public void testPost() {
        System.out.println("Starting test");
        System.out.println("Base URI: " + RestAssured.baseURI);

        Response response = given()
                .baseUri("https://httpbin.org")
                .accept(ContentType.JSON)
                .when()
                .post("/post");

        String className = this.getClass().getSimpleName();
        String methodName = new Object() {
        }.getClass().getEnclosingMethod().getName();
        System.out.println("Response Body for " + className + "." + methodName + ":");
        System.out.println(response.getBody().asPrettyString());

        response.then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("url", equalTo("https://httpbin.org/post"))
                .body("$", hasKey("args"))
                .body("$", hasKey("files"))
                .body("$", hasKey("form"))
                .body("data", equalTo(""))
                .body("json", nullValue())
                .body("origin", not(emptyOrNullString()))
                .header("Access-Control-Allow-Credentials", "true")
                .header("Access-Control-Allow-Origin", "https://httpbin.org")
                .header("Content-Type", "application/json")
                .header("Server", "gunicorn/19.9.0");
    }
}
