<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Services\ProductGatewayController;

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

Route::middleware('auth:sanctum')->group(function () {
    # Gateway routes
    Route::get('/me', [AuthController::class, 'me']);
    Route::post('/logout', [AuthController::class, 'logout']);

    # Product routes
    Route::get('/products', [ProductGatewayController::class, 'index']);
    Route::get('/products/{id}', [ProductGatewayController::class, 'show']);
    Route::post('/products', [ProductGatewayController::class, 'store']);
    Route::put('/products/{id}', [ProductGatewayController::class, 'update']);
    Route::delete('/products/{id}', [ProductGatewayController::class, 'destroy']);
    Route::get('/products/{id}/stock', [ProductGatewayController::class, 'stock']);
    Route::patch('/products/{id}/stock/decrease', [ProductGatewayController::class, 'decreaseStock']);
    Route::patch('/products/{id}/stock/increase', [ProductGatewayController::class, 'increaseStock']);
});
