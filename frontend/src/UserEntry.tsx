export default function UserEntry(){
    return(
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
    <nav className="navbar bg-white navbar-expand-sm d-flex justify-content-between" style={{ width: '80%', height: '60%' }}>
      <input type="text" name="text" className="form-control" placeholder="Type a message..." />
  
      <div className="icondiv d-flex justify-content-end align-content-center text-center ml-2">
        <i className="fa fa-paperclip icon1"></i>
        <i className="fa fa-arrow-circle-right icon2"></i>
      </div>
    </nav>
    <button type="button" className="btn btn-primary" style={{padding:20}}>S</button>
  </div>
  
    );
  }