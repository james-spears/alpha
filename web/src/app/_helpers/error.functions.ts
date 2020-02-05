function hasError(field: string, error:string): boolean {
    try {
      this.f[field].errors[error]
      return true
    } catch(err) {
      return false
    }
}

export { hasError }