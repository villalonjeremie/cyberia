<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Contracts\HttpClient\HttpClientInterface;
use App\Service\PythonPredictionService;

class LogUploadController extends AbstractController
{
    private PythonPredictionService $pythonService;

    public function __construct(PythonPredictionService $pythonService)
    {
        $this->pythonService = $pythonService;
    }

    #[Route('/api/upload-log', name: 'upload_log', methods: ['POST'])]
    public function upload(Request $request): JsonResponse
    {
        $file = $request->files->get('file');

        
        

        if (!$file) {
            return new JsonResponse([
                'error' => 'Aucun fichier reçu'
            ], 400);
        }

        if ($file->getClientOriginalExtension() !== 'log') {
            return new JsonResponse([
                'error' => 'Format invalide'
            ], 400);
        }

        $filePath = $file->getPathname();

        $result = $this->pythonService->sendLogFile($filePath);
        $resultJson = $this->json($result);

        $lines = file(
            $file->getPathname(),
            FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES
        );

        return new JsonResponse([
            'filename' => $file->getClientOriginalName(),
            'count' => count($lines),
            'lines' => $lines,
            'result' => $result
        ]); 
    }

    public function predict(HttpClientInterface $client)
    {
        $response = $client->request(
            'GET',
            'http://log_python_worker:8030/predict',
            [
                'headers' => [
                    'X-API-KEY' => 'SECRET123'
                ]
            ]
        );
        
        var_dump($response);

        $data = $response->toArray();

        return $this->json($data);
    }
}
