<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\HttpFoundation\File\UploadedFile;
use Doctrine\ORM\EntityManagerInterface;
use App\Service\PythonPredictionService;

final class LogController
{
    private PythonPredictionService $pythonService;

    public function __construct(PythonPredictionService $pythonService)
    {
        $this->pythonService = $pythonService;
    }

    #[Route('/api/log',name: 'api_log', methods: ['POST'])]
    public function __invoke(Request $request, EntityManagerInterface $em): JsonResponse
    {
        $dataArray = json_decode($request->getContent(), true);
        $logContent = $dataArray['content'];

        if (empty($dataArray)) {
            return new JsonResponse(
                [
                    'status' => 'error',
                    'message' => 'Empty request body'
                ],
                JsonResponse::HTTP_BAD_REQUEST
            );
        }

       $lines = explode("\n", trim($logContent));

        foreach ($lines as $line) {
            if (!$this->isValidApacheLogLine($line)) {
                return new JsonResponse(
                    [
                        'status' => 'error',
                        'message' => 'Wrong log format',
                        'line' => trim($line)
                    ],
                    JsonResponse::HTTP_UNPROCESSABLE_ENTITY 
                );
            }
        }

        $tempPath = tempnam(sys_get_temp_dir(), 'log_');
        file_put_contents($tempPath, $logContent);

        $file = new UploadedFile(
            $tempPath,
            'access.log',
            'text/plain',
            null,
            true
        );
        
        $originalFinalName = $file->getClientOriginalName();
        $filePath = $file->getPathname();
        $result = $this->pythonService->sendLogFile($filePath, $originalFinalName);

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

    private function isValidApacheLogLine(string $line): bool
    {
        $pattern = '/^(\d{1,3}(?:\.\d{1,3}){3})\s-\s-\s\[\d{2}\/[A-Za-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4}\]\s"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s\/[^"]*\sHTTP\/\d\.\d"\s\d+\s\d+$/';
        return preg_match($pattern, trim($line)) === 1;
    }

            /** 
        if (!is_array($data)) {
            return new JsonResponse(
                ['error' => 'Invalid JSON'],
                400
            );
        }

        $logs = new Logs();
        $logs->setSecurityType($data['type']);
        $logs->setLogsJson($data['content']);
        $logs->setCreatedAt($logs->getCreatedAt());
        $logs->setIsProcessed(false);

        $em->persist($logs);
        $em->flush();

        return new JsonResponse([
            'status' => 'ok',
            'received' => $data,
        ]);**/
}
