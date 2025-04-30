document.addEventListener('DOMContentLoaded', function() {
    // API base URL
    const API_BASE_URL = '/api/v1';

    // Form elements
    const applicantSearchForm = document.getElementById('applicantSearchForm');
    const streetSearchForm = document.getElementById('streetSearchForm');
    const nearestSearchForm = document.getElementById('nearestSearchForm');
    const useCurrentLocationBtn = document.getElementById('useCurrentLocation');
    const resultsContainer = document.getElementById('resultsContainer');

    // Search by applicant name
    applicantSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = document.getElementById('applicantName').value;
        const status = document.getElementById('applicantStatus').value;
        
        if (!name) {
            alert('Please enter an applicant name');
            return;
        }
        let queryString = `?applicant=${name}`
        if (status) {
            queryString = queryString + `&status=${status}`
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/permit${queryString}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error searching by applicant:', error);
            resultsContainer.innerHTML = '<p class="text-danger">Error searching for facilities. Please try again.</p>';
        }
    });

    // Search by street name
    streetSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const street = document.getElementById('streetName').value;
        
        if (!street) {
            alert('Please enter a street name');
            return;
        }
        
        try {
            const queryString = `?address=${street}`
            const response = await fetch(`${API_BASE_URL}/permit${queryString}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error searching by street:', error);
            resultsContainer.innerHTML = '<p class="text-danger">Error searching for facilities. Please try again.</p>';
        }
    });

    // Find nearest food trucks
    nearestSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        const status = document.getElementById('nearestStatus').value;
        
        if (!latitude || !longitude) {
            alert('Please enter latitude and longitude');
            return;
        }

        let queryString = `?latitude=${latitude}&longitude=${longitude}`
        if (status === "APPROVED") {
            queryString = queryString + `&status=${status}`
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/permit${queryString}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error finding nearest facilities');
            }
            
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error finding nearest facilities:', error);
            resultsContainer.innerHTML = `<p class="text-danger">${error.message || 'Error finding nearest facilities. Please try again.'}</p>`;
        }
    });

    // Use current location
    useCurrentLocationBtn.addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    document.getElementById('latitude').value = position.coords.latitude;
                    document.getElementById('longitude').value = position.coords.longitude;
                },
                function(error) {
                    console.error('Error getting location:', error);
                    alert('Unable to retrieve your location. Please enter coordinates manually.');
                }
            );
        } else {
            alert('Geolocation is not supported by your browser. Please enter coordinates manually.');
        }
    });

    function displayResults(facilities) {
        if (!facilities || facilities.length === 0) {
            resultsContainer.innerHTML = '<p class="text-center">No facilities found matching your search criteria.</p>';
            return;
        }

        // Get column headers from the first facility object
        const columns = Object.keys(facilities[0]);

        // Create table structure
        let html = '<div class="table-responsive"><table class="table table-striped">';

        // Add table header
        html += '<thead><tr>';
        columns.forEach(column => {
            html += `<th scope="col">${formatColumnName(column)}</th>`;
        });
        html += '</tr></thead>';

        // Add table body
        html += '<tbody>';
        facilities.forEach(facility => {
            html += '<tr>';
            columns.forEach(column => {
                const value = facility[column] || '';
                html += `<td>${formatCellValue(value)}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table></div>';

        resultsContainer.innerHTML = html;
    }

    function formatColumnName(column) {
        return column
        .split(/(?=[A-Z])/)
        .join(' ')
        .replace(/^\w/, c => c.toUpperCase());
    }

    function formatCellValue(value) {
        if (value === null || value === undefined) {
            return '';
        }
        if (typeof value === 'object') {
            return JSON.stringify(value);
        }
        return value.toString();
    }

});
