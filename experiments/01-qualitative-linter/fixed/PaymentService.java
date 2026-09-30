// Payment service of a demo shop. Invented code for a talk: no real system, every value is fake.
package demo.shop;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PaymentService {
    private static final Logger log = LoggerFactory.getLogger(PaymentService.class);
    private final String gatewayApiKey = System.getenv("GATEWAY_API_KEY");
    private final PaymentGateway gateway = new PaymentGateway();

    public Receipt charge(PaymentRequest request, Customer customer) {
        log.info("Charging card {}", Masker.mask(request.getCardNumber()));
        log.debug("Calling gateway with key {}", Masker.mask(gatewayApiKey));

        long start = System.currentTimeMillis();
        Payment payment = gateway.charge(gatewayApiKey, request);
        long elapsedMs = System.currentTimeMillis() - start;

        log.info("Charged card {}", Masker.mask(request.getCardNumber()));
        log.info("Payment {} settled in {} ms", payment.getId(), elapsedMs);
        System.out.println("Customer phone: " + customer.getPhone());
        return new Receipt(payment);
    }

    static final class Masker {
        /** Hide everything except the last four characters. */
        static String mask(String value) {
            if (value == null) return "null";
            int keep = Math.min(4, value.length());
            return "*".repeat(value.length() - keep) + value.substring(value.length() - keep);
        }
    }
}
