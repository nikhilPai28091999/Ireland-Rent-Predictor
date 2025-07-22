import { useLocation, useNavigate } from "react-router-dom";
import "./Listings.css";

function Listings() {
  const location = useLocation();
  const { predicted_rent, matching_properties } = location.state || {};
  const navigate = useNavigate();

  const handleBack = () => {
    navigate("/chat");
  };

  const handleRowClick = () => {
    window.open("https://www.daft.ie/property-for-rent/ireland", "_blank");
  };

  return (
    <>
      <button className="back-button" onClick={handleBack}>
        ⬅️ Back to Chat
      </button>
      <div className="listings-container">
        <h1>Properties close to €{predicted_rent}</h1>

        {matching_properties?.length > 0 ? (
          <table className="properties-table">
            <thead>
              <tr>
                <th>S.No</th>
                <th>Title</th>
                <th>Location</th>
                <th>Price (€)</th>
              </tr>
            </thead>
            <tbody>
              {matching_properties.map((property, idx) => (
                <tr
                  key={idx}
                  className="clickable-row"
                  onClick={handleRowClick}
                >
                  <td>{idx + 1}</td>
                  <td>{property.Title}</td>
                  <td>{property.location}</td>
                  <td>€{property.Price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No listings available in this price range.</p>
        )}
      </div>
    </>
  );
}

export default Listings;
