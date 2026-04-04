<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Throwable;

class SalesGatewayController extends Controller
{
    public function index(): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function show(string $id): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function store(Request $request): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'userId',
                'productId',
                'productName',
                'quantity',
                'unitPrice',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->post("{$salesServiceUrl}/api/sales", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byUser(int $userId): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/user/{$userId}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byDateRange(Request $request): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $queryParams = $request->only([
                'startDate',
                'endDate',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/date-range/search", $queryParams);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function process(Request $request): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        $productId = $request->input('productId');
        $quantity = $request->input('quantity');
        $user = $request->user();

        if ($productId === null || $quantity === null) {
            return response()->json([
                'message' => 'Los campos productId y quantity son obligatorios.',
            ], 400);
        }

        $parsedProductId = (int) $productId;
        $parsedQuantity = (int) $quantity;

        if ($parsedProductId <= 0) {
            return response()->json([
                'message' => 'El campo productId debe ser un entero positivo.',
            ], 400);
        }

        if ($parsedQuantity <= 0) {
            return response()->json([
                'message' => 'El campo quantity debe ser un entero positivo.',
            ], 400);
        }

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $productResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$catalogServiceUrl}/api/products/{$parsedProductId}");

            if ($productResponse->failed()) {
                return response()->json($productResponse->json(), $productResponse->status());
            }

            $product = $productResponse->json();

            if (
                !is_array($product) ||
                !isset($product['id'], $product['name'], $product['price'], $product['stock'])
            ) {
                return response()->json([
                    'message' => 'La respuesta del microservicio de catálogo e inventario no tiene el formato esperado.',
                ], 502);
            }

            $currentStock = (int) $product['stock'];
            $unitPrice = (float) $product['price'];

            if ($currentStock < $parsedQuantity) {
                return response()->json([
                    'message' => 'Stock insuficiente para procesar la venta.',
                    'product' => [
                        'id' => $product['id'],
                        'name' => $product['name'],
                        'current_stock' => $currentStock,
                        'requested_quantity' => $parsedQuantity,
                    ],
                ], 400);
            }

            $salePayload = [
                'userId' => $user->id,
                'productId' => (int) $product['id'],
                'productName' => $product['name'],
                'quantity' => $parsedQuantity,
                'unitPrice' => $unitPrice,
            ];

            $saleResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$salesServiceUrl}/api/sales", $salePayload);

            if ($saleResponse->failed()) {
                return response()->json($saleResponse->json(), $saleResponse->status());
            }

            $stockResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->patch("{$catalogServiceUrl}/api/products/{$parsedProductId}/stock/decrease", [
                    'quantity' => $parsedQuantity,
                ]);

            if ($stockResponse->failed()) {
                return response()->json([
                    'message' => 'La venta fue registrada, pero no fue posible actualizar el stock.',
                    'sale' => $saleResponse->json()['sale'] ?? null,
                    'stock_error' => $stockResponse->json(),
                ], 502);
            }

            return response()->json([
                'message' => 'Venta procesada correctamente.',
                'sale' => $saleResponse->json()['sale'] ?? null,
                'stock' => $stockResponse->json()['product'] ?? null,
            ], 201);
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible procesar la venta.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }





}
