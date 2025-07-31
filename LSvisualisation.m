
rng(42); % Imposta il seed per la riproducibilità
x = linspace(0, 10, 50)';
y = 2*x + 1 + 2*randn(size(x));

% Calcola la retta di regressione
coefficients = polyfit(x, y, 1);
y_fit = polyval(coefficients, x);

% Calcola lo scarto quadratico
residuals = y - y_fit;
squared_residuals = residuals.^2;
mean_squared_error = mean(squared_residuals);

% Plot dei dati e della retta di regressione
figure;
scatter(x, y, 'o', 'DisplayName', 'Dati');
hold on;
plot(x, y_fit, 'b-', 'LineWidth', 1, 'DisplayName', 'Retta di regressione');
xlabel('X');
ylabel('Y');
title('Retta di Regressione e Scarto Quadratico');

% Evidenzia lo scarto quadratico
for i = 1:length(x)
    line([x(i), x(i)], [y(i), y_fit(i)], 'Color', [1 0 0], 'LineWidth', 2);
end

hold off;

% Mostra lo scarto quadratico medio
disp(['Scarto quadratico medio: ', num2str(mean_squared_error)]);

